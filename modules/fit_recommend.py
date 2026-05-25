# -*- coding: utf-8 -*-
"""
公差配合推荐模块
"""

import streamlit as st
import pandas as pd

from data.fit_data import COMMON_FITS_INFO, FIT_RECOMMENDATION_RULES
from modules.utils import query_tolerance, format_deviation, generate_tolerance_zone_svg


def render_fit_recommendation_tab():
    """渲染配合推荐选项卡"""
    st.markdown("## 🎯 公差配合推荐")

    with st.form("fit_recommendation_form"):
        col1, col2 = st.columns(2)
        fit_type = col1.selectbox("配合类型", options=["轴孔配合"], index=0)
        basic_size = col2.number_input("基本尺寸 (mm)", value=50.0, min_value=0.1, max_value=500.0, step=0.1)

        col3, col4, col5 = st.columns(3)
        load_level = col3.selectbox("载荷等级", options=["轻载", "中载", "重载"], index=0)
        speed_level = col4.selectbox("转速等级", options=["低速", "中速", "高速"], index=0)
        precision_level = col5.selectbox("定心精度", options=["一般", "较高", "高精度"], index=0)

        col6, col7 = st.columns(2)
        disassembly_req = col6.selectbox("拆卸要求", options=["频繁拆卸", "偶尔拆卸", "不拆卸", "永久装配", "自由装配"], index=0)
        system_basis = col7.selectbox("优先制度", options=["基孔制", "基轴制"], index=0)

        submitted = st.form_submit_button("🔍 获取推荐配合", type="primary", use_container_width=True)

    if submitted:
        # 推荐引擎：匹配规则
        user_conditions = {
            "load": load_level,
            "speed": speed_level,
            "precision": precision_level,
            "disassembly": disassembly_req,
        }

        scored_rules = []
        for rule in FIT_RECOMMENDATION_RULES:
            match_count = 0
            total_conditions = len(rule["conditions"])
            for key, value in rule["conditions"].items():
                if key in user_conditions and user_conditions[key] == value:
                    match_count += 1
            scored_rules.append({
                "rule": rule,
                "match_count": match_count,
                "match_ratio": match_count / total_conditions if total_conditions > 0 else 0,
            })

        # 按匹配数排序，取前3
        scored_rules.sort(key=lambda x: x["match_count"], reverse=True)
        top_rules = scored_rules[:3]

        if not top_rules or top_rules[0]["match_count"] == 0:
            st.warning("未找到完全匹配的推荐规则，以下为最接近的推荐：")

        # 收集所有推荐的配合代号（去重）
        all_recommended_fits = []
        seen_fits = set()
        for sr in top_rules:
            for fit in sr["rule"]["fits"]:
                if fit not in seen_fits:
                    all_recommended_fits.append({
                        "fit": fit,
                        "rule": sr["rule"],
                        "match_count": sr["match_count"],
                    })
                    seen_fits.add(fit)

        # 显示推荐结果
        for idx, rec in enumerate(all_recommended_fits[:3]):
            fit_designation = rec["fit"]
            rule = rec["rule"]

            st.markdown(f"### 推荐 {idx + 1}: {fit_designation}")

            # 查询实际偏差值
            hole_letter = fit_designation[0].upper()
            shaft_letter = fit_designation.split("/")[1][0].lower() if "/" in fit_designation else None

            # 解析配合代号
            parts = fit_designation.split("/")
            hole_desig = parts[0] if len(parts) > 0 else None
            shaft_desig = parts[1] if len(parts) > 1 else None

            col_info, col_detail = st.columns([1, 1])

            with col_info:
                # 从COMMON_FITS_INFO获取信息
                if fit_designation in COMMON_FITS_INFO:
                    fit_info = COMMON_FITS_INFO[fit_designation]
                    st.info(f"**类型:** {fit_info['type']}")
                    st.write(f"**说明:** {fit_info['description']}")
                    st.write(f"**装配方式:** {fit_info['assembly']}")
                else:
                    st.info("配合信息")

                st.write(f"**匹配条件:** {rec['match_count']}/{len(rule['conditions'])}")
                st.write(f"**推荐理由:** {rule['reason']}")

            with col_detail:
                # 计算实际偏差值
                if hole_desig and shaft_desig:
                    hole_result = query_tolerance(hole_desig, basic_size)
                    shaft_result = query_tolerance(shaft_desig, basic_size)

                    if hole_result and shaft_result:
                        st.markdown("**实际偏差值:**")
                        st.write(f"孔 {hole_desig}: ES={format_deviation(hole_result['ES'])}, EI={format_deviation(hole_result['EI'])}")
                        st.write(f"轴 {shaft_desig}: es={format_deviation(shaft_result['ES'])}, ei={format_deviation(shaft_result['EI'])}")

                        max_clearance = hole_result["max_size"] - shaft_result["min_size"]
                        min_clearance_max_int = hole_result["min_size"] - shaft_result["max_size"]

                        if min_clearance_max_int >= 0:
                            st.write(f"最大间隙: {max_clearance*1000:.1f} μm")
                            st.write(f"最小间隙: {min_clearance_max_int*1000:.1f} μm")
                        elif max_clearance <= 0:
                            st.write(f"最大过盈: {abs(min_clearance_max_int)*1000:.1f} μm")
                            st.write(f"最小过盈: {abs(max_clearance)*1000:.1f} μm")
                        else:
                            st.write(f"最大间隙: {max_clearance*1000:.1f} μm")
                            st.write(f"最大过盈: {abs(min_clearance_max_int)*1000:.1f} μm")

                # 推荐表面粗糙度
                st.markdown("**推荐表面粗糙度:**")
                if hole_result:
                    hole_grade = int(hole_desig[1:]) if len(hole_desig) > 1 else 7
                    if hole_grade <= 5:
                        ra_hole = "0.4~0.8"
                    elif hole_grade <= 7:
                        ra_hole = "0.8~1.6"
                    elif hole_grade <= 9:
                        ra_hole = "1.6~3.2"
                    else:
                        ra_hole = "3.2~6.3"
                    st.write(f"孔: Ra {ra_hole} μm")

                if shaft_result:
                    shaft_grade = int(shaft_desig[1:]) if len(shaft_desig) > 1 else 6
                    if shaft_grade <= 5:
                        ra_shaft = "0.2~0.4"
                    elif shaft_grade <= 7:
                        ra_shaft = "0.4~0.8"
                    elif shaft_grade <= 9:
                        ra_shaft = "0.8~1.6"
                    else:
                        ra_shaft = "1.6~3.2"
                    st.write(f"轴: Ra {ra_shaft} μm")

                # 推荐形位公差
                st.markdown("**推荐形位公差:**")
                st.write("- 圆柱度: 6~8级")
                st.write("- 同轴度: 6~8级")
                st.write("- 圆跳动: 7~9级")

            st.markdown("---")

        # 复制所有推荐
        copy_lines = ["=== 公差配合推荐结果 ==="]
        copy_lines.append(f"基本尺寸: {basic_size} mm")
        copy_lines.append(f"载荷: {load_level}, 转速: {speed_level}, 精度: {precision_level}")
        copy_lines.append(f"拆卸要求: {disassembly_req}, 制度: {system_basis}")
        copy_lines.append("")
        for idx, rec in enumerate(all_recommended_fits[:3]):
            fit_designation = rec["fit"]
            copy_lines.append(f"推荐{idx+1}: {fit_designation}")
            copy_lines.append(f"  推荐理由: {rec['rule']['reason']}")
            if fit_designation in COMMON_FITS_INFO:
                fi = COMMON_FITS_INFO[fit_designation]
                copy_lines.append(f"  类型: {fi['type']}")
                copy_lines.append(f"  说明: {fi['description']}")
                copy_lines.append(f"  装配方式: {fi['assembly']}")
            copy_lines.append("")

        st.code("\n".join(copy_lines), language="text")

    # 常用配合参考表
    with st.expander("📖 常用配合参考表"):
        ref_data = []
        for key, info in COMMON_FITS_INFO.items():
            ref_data.append({
                "配合代号": key,
                "类型": info["type"],
                "说明": info["description"],
                "装配方式": info["assembly"],
            })
        df_ref = pd.DataFrame(ref_data)
        st.dataframe(df_ref, use_container_width=True, hide_index=True)


