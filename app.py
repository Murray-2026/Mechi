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

# 导航分类定义
NAV_CATEGORIES = [
    {
        "title": "📏 基础计算",
        "items": ["尺寸链计算", "公差查询"],
    },
    {
        "title": "🎯 配合与形位公差",
        "items": ["公差配合推荐", "形位公差推荐"],
    },
    {
        "title": "📐 GD&T 高级",
        "items": ["GD&T 可视化", "基准体系", "公差原则"],
    },
    {
        "title": "🤖 智能工具",
        "items": ["智能推荐", "工程工具"],
    },
    {
        "title": "📚 标准查阅",
        "items": ["标准查阅"],
    },
]

# 页面名称 → 渲染函数映射
PAGE_RENDERERS = {
    "尺寸链计算": render_dimension_chain_tab,
    "公差查询": render_tolerance_query_tab,
    "公差配合推荐": render_fit_recommendation_tab,
    "形位公差推荐": render_geometric_tolerance_tab,
    "GD&T 可视化": render_gdt_visual_tab,
    "基准体系": render_datum_system_tab,
    "公差原则": render_tolerance_principle_tab,
    "智能推荐": render_smart_recommend_tab,
    "工程工具": render_engineering_tools_tab,
    "标准查阅": render_standard_reference_tab,
}


def _apply_theme():
    """应用深色/浅色主题"""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    theme = st.session_state.theme

    if theme == "dark":
        bg_color = "#0e1117"
        text_color = "#fafafa"
        secondary_bg = "#262730"
        accent_color = "#4c8bf5"
    else:
        bg_color = "#ffffff"
        text_color = "#31333f"
        secondary_bg = "#f0f2f6"
        accent_color = "#ff4b4b"

    st.markdown(f"""
    <style>
    /* 全局背景和文字颜色 */
    .stApp, [data-testid="stMainBlockContainer"] {{
        background-color: {bg_color} !important;
    }}
    [data-testid="stMainBlockContainer"] {{
        color: {text_color};
    }}
    /* 侧边栏 */
    [data-testid="stSidebar"] {{
        background-color: {secondary_bg} !important;
    }}
    /* 主标题 */
    .main-header {{
        background: linear-gradient(135deg, {accent_color}, #764ba2);
        color: white;
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 24px;
        text-align: center;
    }}
    .main-header h1 {{
        margin: 0 0 8px 0;
        font-size: 28px;
        font-weight: 700;
    }}
    .main-header p {{
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
    }}
    /* 页脚 */
    .disclaimer {{
        background: {'#1a1a2e' if theme == 'dark' else '#fff3cd'};
        color: {'#fafafa' if theme == 'dark' else '#856404'};
        padding: 12px 20px;
        border-radius: 8px;
        margin-top: 40px;
        text-align: center;
        font-size: 13px;
    }}
    /* 按钮样式 */
    .stButton > button {{
        border-radius: 8px;
    }}
    /* 选项卡样式 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
    }}
    /* 数据框样式 */
    [data-testid="stDataFrame"] {{
        border-radius: 8px;
    }}
    /* 指标卡片 */
    [data-testid="stMetric"] {{
        background: {secondary_bg};
        padding: 16px;
        border-radius: 10px;
    }}
    /* 滚动条 */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {secondary_bg};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {accent_color};
        border-radius: 4px;
    }}
    </style>
    """, unsafe_allow_html=True)


def _build_sidebar_nav(current_page):
    """构建侧边栏分类导航，全局只有一个选中项"""
    # 初始化主题
    _apply_theme()

    st.sidebar.markdown("## ⚙️ 导航菜单")

    # 主题切换
    theme_col1, theme_col2 = st.sidebar.columns([1, 1])
    with theme_col1:
        if st.button("☀️ 浅色", key="theme_light", use_container_width=True,
                     type="primary" if st.session_state.get("theme") == "light" else "secondary"):
            st.session_state.theme = "light"
            st.rerun()
    with theme_col2:
        if st.button("🌙 深色", key="theme_dark", use_container_width=True,
                     type="primary" if st.session_state.get("theme") == "dark" else "secondary"):
            st.session_state.theme = "dark"
            st.rerun()

    st.sidebar.markdown("---")

    for cat in NAV_CATEGORIES:
        st.sidebar.markdown("### " + cat["title"])
        for item in cat["items"]:
            is_active = (item == current_page)
            if is_active:
                btn_type = "primary"
            else:
                btn_type = "secondary"
            if st.sidebar.button(item, key=f"nav_{item}", use_container_width=True, type=btn_type):
                st.session_state.current_page = item
                st.rerun()
        st.sidebar.markdown("---")


def main():
    """主函数：构建Streamlit应用界面"""

    # 初始化当前页面
    if "current_page" not in st.session_state:
        st.session_state.current_page = "尺寸链计算"

    # 初始化主题
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # 构建侧边栏导航
    _build_sidebar_nav(st.session_state.current_page)

    # ===== 主内容区 =====
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ 机械公差助手</h1>
        <p>基于 GB/T 1800 / GB/T 1182 / ASME Y14.5 / ISO 2768 国家与国际标准 | v3.1</p>
    </div>
    """, unsafe_allow_html=True)

    # 渲染当前页面
    renderer = PAGE_RENDERERS.get(st.session_state.current_page)
    if renderer:
        renderer()

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
