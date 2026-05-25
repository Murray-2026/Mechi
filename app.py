# -*- coding: utf-8 -*-
"""
机械公差助手 - 主入口
基于 GB/T 1800、GB/T 1182、ASME Y14.5、ISO 2768 等标准
"""

import streamlit as st

from modules.dimension_chain import render_dimension_chain_tab
from modules.tolerance_query import render_tolerance_query_tab
from modules.fit_recommend import render_fit_recommendation_tab
from modules.geo_tolerance import render_geometric_tolerance_tab
from modules.standard_reference import render_standard_reference_tab
from modules.gdt_visual import render_gdt_visual_tab
from modules.datum_system import render_datum_system_tab
from modules.tolerance_principle import render_tolerance_principle_tab
from modules.smart_recommend import render_smart_recommend_tab
from modules.engineering_tools import render_engineering_tools_tab


def main():
    """主函数：构建Streamlit应用界面"""

    # ===== 侧边栏分类导航 =====
    st.sidebar.markdown("## ⚙️ 导航菜单")
    st.sidebar.markdown("---")

    # 记录每个分类的选中项
    pages = {}

    # 第一类：基础计算
    st.sidebar.markdown("### 📏 基础计算")
    pages["尺寸链计算"] = st.sidebar.radio(
        "", ["尺寸链计算", "公差查询"], label_visibility="collapsed", key="nav_basic"
    )

    st.sidebar.markdown("---")

    # 第二类：配合与形位公差
    st.sidebar.markdown("### 🎯 配合与形位公差")
    pages["公差配合推荐"] = st.sidebar.radio(
        "", ["公差配合推荐", "形位公差推荐"], label_visibility="collapsed", key="nav_fit_geo"
    )

    st.sidebar.markdown("---")

    # 第三类：GD&T 高级
    st.sidebar.markdown("### 📐 GD&T 高级")
    pages["GD&T 可视化"] = st.sidebar.radio(
        "", ["GD&T 可视化", "基准体系", "公差原则"], label_visibility="collapsed", key="nav_gdt"
    )

    st.sidebar.markdown("---")

    # 第四类：智能工具
    st.sidebar.markdown("### 🤖 智能工具")
    pages["智能推荐"] = st.sidebar.radio(
        "", ["智能推荐", "工程工具"], label_visibility="collapsed", key="nav_tool"
    )

    st.sidebar.markdown("---")

    # 第五类：标准查阅
    st.sidebar.markdown("### 📚 标准查阅")
    pages["标准查阅"] = st.sidebar.radio(
        "", ["标准查阅"], label_visibility="collapsed", key="nav_std"
    )

    # 用 session_state 追踪最近点击的分类
    # Streamlit radio 每次交互都会触发 rerun，我们通过比较前后值来判断哪个被点击了
    if "last_active_category" not in st.session_state:
        st.session_state.last_active_category = "nav_basic"

    # 检查哪个分类的值发生了变化（即用户点击了该分类下的选项）
    for cat_key in ["nav_basic", "nav_fit_geo", "nav_gdt", "nav_tool", "nav_std"]:
        if st.session_state.get(cat_key + "_prev") != st.session_state.get(cat_key):
            st.session_state.last_active_category = cat_key

    # 保存当前值供下次比较
    for cat_key in ["nav_basic", "nav_fit_geo", "nav_gdt", "nav_tool", "nav_std"]:
        st.session_state[cat_key + "_prev"] = st.session_state.get(cat_key)

    # 根据最近活跃的分类确定当前页面
    active_cat = st.session_state.last_active_category
    if active_cat == "nav_basic":
        current_page = st.session_state.nav_basic
    elif active_cat == "nav_fit_geo":
        current_page = st.session_state.nav_fit_geo
    elif active_cat == "nav_gdt":
        current_page = st.session_state.nav_gdt
    elif active_cat == "nav_tool":
        current_page = st.session_state.nav_tool
    elif active_cat == "nav_std":
        current_page = st.session_state.nav_std
    else:
        current_page = "尺寸链计算"

    # ===== 主内容区 =====
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ 机械公差助手</h1>
        <p>基于 GB/T 1800 / GB/T 1182 / ASME Y14.5 / ISO 2768 国家与国际标准 | v3.0</p>
    </div>
    """, unsafe_allow_html=True)

    # 根据选择渲染对应模块
    if current_page == "尺寸链计算":
        render_dimension_chain_tab()
    elif current_page == "公差查询":
        render_tolerance_query_tab()
    elif current_page == "公差配合推荐":
        render_fit_recommendation_tab()
    elif current_page == "形位公差推荐":
        render_geometric_tolerance_tab()
    elif current_page == "GD&T 可视化":
        render_gdt_visual_tab()
    elif current_page == "基准体系":
        render_datum_system_tab()
    elif current_page == "公差原则":
        render_tolerance_principle_tab()
    elif current_page == "智能推荐":
        render_smart_recommend_tab()
    elif current_page == "工程工具":
        render_engineering_tools_tab()
    elif current_page == "标准查阅":
        render_standard_reference_tab()

    # 页脚免责声明
    st.markdown("""
    <div class="disclaimer">
        ⚠️ 免责声明：本工具计算结果仅供参考，关键设计请以国家标准和设计手册为准。
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    main()
