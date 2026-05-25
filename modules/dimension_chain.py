# -*- coding: utf-8 -*-
"""
尺寸链计算模块
"""

import streamlit as st
import pandas as pd

from modules.utils import (
    calculate_dimension_chain,
    generate_dimension_chain_svg,
)


def render_dimension_chain_tab():
    """渲染尺寸链计算选项卡"""
    st.markdown("## 📏 尺寸链计算（极值法）")

    # 初始化session_state中的组成环列表
    if "dim_chain_components" not in st.session_state:
        st.session_state.dim_chain_components = [
            {"name": "A1", "basic_size": 50.0, "upper_dev": 0.0, "lower_dev": -0.1, "ring_type": "增环"},
            {"name": "A2", "basic_size": 30.0, "upper_dev": 0.05, "lower_dev": -0.05, "ring_type": "减环"},
            {"name": "A3", "basic_size": 20.0, "upper_dev": 0.05, "lower_dev": -0.05, "ring_type": "增环"},
        ]

    # 显示尺寸链示意图
    st.markdown("### 尺寸链示意图")
    svg_diagram = generate_dimension_chain_svg(st.session_state.dim_chain_components)
    st.markdown(svg_diagram, unsafe_allow_html=True)
    st.caption("💡 示意图说明：第一个组成环（A1）为总尺寸显示在上方，其余组成环为分段尺寸显示在下方，A₀为封闭环间隙")

    st.markdown("---")

    # 显示各组成环输入行
    st.markdown("### 输入组成环")
    cols_header = st.columns([2, 2, 2, 2, 2, 1])
    cols_header[0].markdown("**名称**")
    cols_header[1].markdown("**基本尺寸(mm)**")
    cols_header[2].markdown("**上偏差(mm)**")
    cols_header[3].markdown("**下偏差(mm)**")
    cols_header[4].markdown("**环类型**")
    cols_header[5].markdown("**操作**")

    components_to_remove = []
    for i, comp in enumerate(st.session_state.dim_chain_components):
        cols = st.columns([2, 2, 2, 2, 2, 1])
        comp["name"] = cols[0].text_input("名称", value=comp["name"], key=f"comp_name_{i}", label_visibility="collapsed")
        comp["basic_size"] = cols[1].number_input("基本尺寸", value=comp["basic_size"], key=f"comp_size_{i}", label_visibility="collapsed", step=0.1)
        comp["upper_dev"] = cols[2].number_input("上偏差", value=comp["upper_dev"], key=f"comp_upper_{i}", label_visibility="collapsed", step=0.001, format="%.3f")
        comp["lower_dev"] = cols[3].number_input("下偏差", value=comp["lower_dev"], key=f"comp_lower_{i}", label_visibility="collapsed", step=0.001, format="%.3f")
        comp["ring_type"] = cols[4].selectbox("环类型", options=["增环", "减环"], index=0 if comp["ring_type"] == "增环" else 1, key=f"comp_type_{i}", label_visibility="collapsed")
        if cols[5].button("删除", key=f"comp_del_{i}"):
            components_to_remove.append(i)

    # 删除标记的组成环
    if components_to_remove:
        st.session_state.dim_chain_components = [
            c for i, c in enumerate(st.session_state.dim_chain_components)
            if i not in components_to_remove
        ]
        st.rerun()

    # 添加组成环按钮
    col_add, col_info = st.columns([1, 3])
    if col_add.button("➕ 添加组成环", disabled=len(st.session_state.dim_chain_components) >= 10, key="add_comp_btn"):
        n = len(st.session_state.dim_chain_components) + 1
        st.session_state.dim_chain_components.append({
            "name": f"A{n}",
            "basic_size": 10.0,
            "upper_dev": 0.0,
            "lower_dev": -0.1,
            "ring_type": "增环",
        })
        st.rerun()
    if len(st.session_state.dim_chain_components) >= 10:
        col_info.warning("最多支持10个组成环")

    st.markdown("---")

    # 开始计算按钮
    if st.button("🚀 开始计算", type="primary", use_container_width=True):
        components = st.session_state.dim_chain_components

        # 输入验证
        has_error = False
        for comp in components:
            if comp["basic_size"] <= 0:
                st.error(f"组成环 {comp['name']} 的基本尺寸必须大于0")
                has_error = True
            if comp["upper_dev"] < comp["lower_dev"]:
                st.error(f"组成环 {comp['name']} 的上偏差({comp['upper_dev']})不能小于下偏差({comp['lower_dev']})")
                has_error = True
            if not comp["name"].strip():
                st.error("所有组成环必须有名称")
                has_error = True

        if has_error:
            return

        # 执行计算
        result = calculate_dimension_chain(components)

        # 显示结果
        st.markdown("### 计算结果")
        st.success("尺寸链计算完成")

        # 4个指标卡片
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("封闭环基本尺寸", f"{result['A0']:.3f} mm")
        col2.metric("上偏差", f"{result['ES0']:+.3f} mm")
        col3.metric("下偏差", f"{result['EI0']:+.3f} mm")
        col4.metric("公差值", f"{result['T0']:.3f} mm")

        # 组成环详情表格
        st.markdown("#### 组成环详情")
        table_data = []
        for c in result["contributions"]:
            table_data.append({
                "名称": c["name"],
                "环类型": c["ring_type"],
                "基本尺寸(mm)": c["basic_size"],
                "公差(mm)": f"{c['tolerance']:.3f}",
                "贡献": c["contribution"],
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 计算过程
        st.markdown("#### 计算过程")
        st.code(result["details"], language="text")

        # 复制结果按钮
        copy_text = (
            f"=== 尺寸链计算结果 ===\n"
            f"封闭环基本尺寸: {result['A0']:.3f} mm\n"
            f"上偏差: {result['ES0']:+.3f} mm\n"
            f"下偏差: {result['EI0']:+.3f} mm\n"
            f"公差值: {result['T0']:.3f} mm\n"
            f"最大极限尺寸: {result['A0_max']:.3f} mm\n"
            f"最小极限尺寸: {result['A0_min']:.3f} mm\n"
            f"\n{result['details']}"
        )
        st.code(copy_text, language="text")
