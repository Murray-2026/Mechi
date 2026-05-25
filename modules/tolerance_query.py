# -*- coding: utf-8 -*-
"""
公差查询模块
"""

import streamlit as st
import pandas as pd

from modules.utils import (
    query_tolerance,
    format_deviation,
    generate_tolerance_zone_svg,
)
from data.tolerance_data import SIZE_RANGES, IT_VALUES
from data.fit_data import COMMON_FITS_INFO


def render_tolerance_query_tab():
    """渲染公差查询选项卡"""
    st.markdown("## 🔍 公差查询")

    # 输入区域
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    nominal_size = col1.number_input("公称尺寸 (mm)", value=50.0, min_value=0.1, max_value=500.0, step=0.1)
    hole_designation = col2.text_input("孔公差带代号", value="H7", placeholder="如 H7")
    shaft_designation = col3.text_input("轴公差带代号", value="f6", placeholder="如 f6")
    query_btn = col4.button("🔍 查询")

    if query_btn:
        hole_info = None
        shaft_info = None

        # 查询孔公差
        if hole_designation.strip():
            hole_info = query_tolerance(hole_designation.strip(), nominal_size)
            if hole_info is None:
                st.error(f"孔公差带代号 '{hole_designation}' 无效或公称尺寸超出范围")

        # 查询轴公差
        if shaft_designation.strip():
            shaft_info = query_tolerance(shaft_designation.strip(), nominal_size)
            if shaft_info is None:
                st.error(f"轴公差带代号 '{shaft_designation}' 无效或公称尺寸超出范围")

        if hole_info is None and shaft_info is None:
            st.warning("请至少输入一个有效的公差带代号")
            return

        # 同时提供孔和轴信息时，显示配合分析
        if hole_info is not None and shaft_info is not None:
            st.markdown("### 查询结果")

            # 两列显示孔和轴信息
            col_h, col_s = st.columns(2)

            with col_h:
                st.markdown("#### 🔴 孔信息")
                st.metric("代号", hole_info["designation"])
                st.write(f"**上偏差 (ES):** {format_deviation(hole_info['ES'])} mm")
                st.write(f"**下偏差 (EI):** {format_deviation(hole_info['EI'])} mm")
                st.write(f"**公差 (IT):** {hole_info['IT']} μm = {hole_info['IT']/1000:.3f} mm")
                st.write(f"**最大极限尺寸:** {hole_info['max_size']:.3f} mm")
                st.write(f"**最小极限尺寸:** {hole_info['min_size']:.3f} mm")

            with col_s:
                st.markdown("#### 🔵 轴信息")
                st.metric("代号", shaft_info["designation"])
                st.write(f"**上偏差 (es):** {format_deviation(shaft_info['ES'])} mm")
                st.write(f"**下偏差 (ei):** {format_deviation(shaft_info['EI'])} mm")
                st.write(f"**公差 (IT):** {shaft_info['IT']} μm = {shaft_info['IT']/1000:.3f} mm")
                st.write(f"**最大极限尺寸:** {shaft_info['max_size']:.3f} mm")
                st.write(f"**最小极限尺寸:** {shaft_info['min_size']:.3f} mm")

            # 配合分析
            st.markdown("---")
            st.markdown("#### 配合分析")

            # 最大间隙 = 孔最大 - 轴最小
            max_clearance = hole_info["max_size"] - shaft_info["min_size"]
            # 最小间隙 / 最大过盈 = 孔最小 - 轴最大
            min_clearance_max_interference = hole_info["min_size"] - shaft_info["max_size"]

            if min_clearance_max_interference >= 0:
                fit_type = "间隙配合"
                st.success(f"**配合类型:** {fit_type}")
                st.write(f"**最大间隙 (X_max):** {max_clearance*1000:.1f} μm = {max_clearance:.3f} mm")
                st.write(f"**最小间隙 (X_min):** {min_clearance_max_interference*1000:.1f} μm = {min_clearance_max_interference:.3f} mm")
            elif max_clearance <= 0:
                fit_type = "过盈配合"
                st.error(f"**配合类型:** {fit_type}")
                st.write(f"**最大过盈 (Y_max):** {abs(min_clearance_max_interference)*1000:.1f} μm = {abs(min_clearance_max_interference):.3f} mm")
                st.write(f"**最小过盈 (Y_min):** {abs(max_clearance)*1000:.1f} μm = {abs(max_clearance):.3f} mm")
            else:
                fit_type = "过渡配合"
                st.warning(f"**配合类型:** {fit_type}")
                st.write(f"**最大间隙 (X_max):** {max_clearance*1000:.1f} μm = {max_clearance:.3f} mm")
                st.write(f"**最大过盈 (Y_max):** {abs(min_clearance_max_interference)*1000:.1f} μm = {abs(min_clearance_max_interference):.3f} mm")

            # 查找常用配合信息
            fit_key_hole = hole_info["designation"].upper()
            fit_key_shaft = shaft_info["designation"].lower()
            fit_key = f"{fit_key_hole}/{fit_key_shaft}"
            # 也尝试基轴制形式
            fit_key_alt = None
            if shaft_info["designation"].lower() == "h6":
                # 基轴制: 查找 孔大写/轴小写
                pass
            # 尝试多种组合
            possible_keys = [
                f"{fit_key_hole}/{fit_key_shaft}",
                f"{fit_key_hole}/{shaft_info['designation']}",
            ]

            fit_info_found = None
            for key in possible_keys:
                if key in COMMON_FITS_INFO:
                    fit_info_found = COMMON_FITS_INFO[key]
                    break

            if fit_info_found:
                st.markdown("#### 应用场景")
                st.info(fit_info_found["description"])
                st.write("**典型应用:**")
                for app in fit_info_found["applications"]:
                    st.write(f"- {app}")
                st.write(f"**装配方式:** {fit_info_found['assembly']}")

            st.caption("数据来源: GB/T 1800.1-2020, GB/T 1801-2009")

            # 公差带图
            st.markdown("---")
            st.markdown("#### 📊 公差带图")
            tolerance_svg = generate_tolerance_zone_svg(hole_info, shaft_info, nominal_size)
            col_left, col_right = st.columns([2, 3])
            with col_left:
                st.markdown(tolerance_svg, unsafe_allow_html=True)
            with col_right:
                st.caption("""
**图例说明：**
- 🔴 **红色矩形**：孔公差带（H系列）
- 🔵 **蓝色矩形**：轴公差带
- **黑色粗线**：零线（基本尺寸）
- **左侧标注**：孔偏差 ES（上）、EI（下）
- **右侧标注**：轴偏差 es（上）、ei（下）
- **橙色虚线**：最大间隙/过盈
                """)

            # 复制结果
            copy_text = (
                f"=== 公差查询结果 ===\n"
                f"公称尺寸: {nominal_size} mm\n"
                f"\n孔: {hole_info['designation']}\n"
                f"  ES = {format_deviation(hole_info['ES'])} mm\n"
                f"  EI = {format_deviation(hole_info['EI'])} mm\n"
                f"  IT = {hole_info['IT']} μm\n"
                f"  最大尺寸: {hole_info['max_size']:.3f} mm\n"
                f"  最小尺寸: {hole_info['min_size']:.3f} mm\n"
                f"\n轴: {shaft_info['designation']}\n"
                f"  es = {format_deviation(shaft_info['ES'])} mm\n"
                f"  ei = {format_deviation(shaft_info['EI'])} mm\n"
                f"  IT = {shaft_info['IT']} μm\n"
                f"  最大尺寸: {shaft_info['max_size']:.3f} mm\n"
                f"  最小尺寸: {shaft_info['min_size']:.3f} mm\n"
                f"\n配合类型: {fit_type}\n"
            )
            if fit_info_found:
                copy_text += f"说明: {fit_info_found['description']}\n"
                copy_text += f"装配方式: {fit_info_found['assembly']}\n"
            st.code(copy_text, language="text")

        else:
            # 只提供一个公差带代号
            st.markdown("### 查询结果")
            info = hole_info if hole_info else shaft_info
            type_label = "孔" if info["type"] == "hole" else "轴"
            es_label = "ES" if info["type"] == "hole" else "es"
            ei_label = "EI" if info["type"] == "hole" else "ei"

            st.metric(f"{type_label}公差带代号", info["designation"])
            st.write(f"**{es_label} (上偏差):** {format_deviation(info['ES'])} mm")
            st.write(f"**{ei_label} (下偏差):** {format_deviation(info['EI'])} mm")
            st.write(f"**公差 (IT):** {info['IT']} μm = {info['IT']/1000:.3f} mm")
            st.write(f"**最大极限尺寸:** {info['max_size']:.3f} mm")
            st.write(f"**最小极限尺寸:** {info['min_size']:.3f} mm")

            copy_text = (
                f"=== 公差查询结果 ===\n"
                f"公称尺寸: {nominal_size} mm\n"
                f"{type_label}: {info['designation']}\n"
                f"  {es_label} = {format_deviation(info['ES'])} mm\n"
                f"  {ei_label} = {format_deviation(info['EI'])} mm\n"
                f"  IT = {info['IT']} μm\n"
                f"  最大尺寸: {info['max_size']:.3f} mm\n"
                f"  最小尺寸: {info['min_size']:.3f} mm\n"
            )
            st.code(copy_text, language="text")

    # IT等级参考表
    with st.expander("📖 IT等级参考表"):
        st.markdown("标准公差等级 (GB/T 1800.1-2020)")
        # 构建参考表
        it_ref_data = []
        for grade_name in ["IT01", "IT0", "IT1", "IT2", "IT3", "IT4", "IT5", "IT6", "IT7", "IT8", "IT9", "IT10", "IT11", "IT12"]:
            vals = IT_VALUES[grade_name]
            # 取中间尺寸段(30-50mm)的值作为参考
            it_ref_data.append({
                "等级": grade_name,
                "0~3mm": vals[0],
                "3~6mm": vals[1],
                "6~10mm": vals[2],
                "10~18mm": vals[3],
                "18~30mm": vals[4],
                "30~50mm": vals[5],
                "50~80mm": vals[6],
                "80~120mm": vals[7],
                "120~180mm": vals[8],
                "180~250mm": vals[9],
            })
        df_it = pd.DataFrame(it_ref_data)
        st.dataframe(df_it, use_container_width=True, hide_index=True)
        st.caption("单位: 微米 (μm)")
