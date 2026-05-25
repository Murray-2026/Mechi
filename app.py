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
    # 页面标题
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ 机械公差助手</h1>
        <p>基于 GB/T 1800 / GB/T 1182 / ASME Y14.5 / ISO 2768 国家与国际标准 | v3.0</p>
    </div>
    """, unsafe_allow_html=True)

    # 创建选项卡
    tabs = st.tabs([
        "📏 尺寸链计算",
        "🔍 公差查询",
        "🎯 公差配合推荐",
        "📐 形位公差推荐",
        "📚 标准查阅",
        "🎯 GD&T 可视化",
        "📐 基准体系",
        "📐 公差原则",
        "🤖 智能推荐",
        "🔧 工程工具",
    ])

    with tabs[0]:
        render_dimension_chain_tab()

    with tabs[1]:
        render_tolerance_query_tab()

    with tabs[2]:
        render_fit_recommendation_tab()

    with tabs[3]:
        render_geometric_tolerance_tab()

    with tabs[4]:
        render_standard_reference_tab()

    with tabs[5]:
        render_gdt_visual_tab()

    with tabs[6]:
        render_datum_system_tab()

    with tabs[7]:
        render_tolerance_principle_tab()

    with tabs[8]:
        render_smart_recommend_tab()

    with tabs[9]:
        render_engineering_tools_tab()

    # 页脚免责声明
    st.markdown("""
    <div class="disclaimer">
        ⚠️ 免责声明：本工具计算结果仅供参考，关键设计请以国家标准和设计手册为准。
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 入口
# ============================================================
