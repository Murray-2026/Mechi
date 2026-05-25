# -*- coding: utf-8 -*-
"""
标准查阅模块
"""

import streamlit as st

from data.standard_data import _build_glossary, _search_glossary
from data.tolerance_data import SIZE_RANGES, IT_VALUES


def render_standard_reference_tab():
    """渲染标准查阅选项卡 - 基于内置数据查询 GB/T 标准内容"""
    st.markdown("## 📚 国家标准查阅")
    st.markdown("基于应用内置的标准数据，查询 GB/T 1800、GB/T 1182、GB/T 17851、GB/T 4249、GB/T 45683 等国家标准的完整内容")

    # 构建术语词典
    glossary = _build_glossary()

    # 标准选择 + 阅读模式切换
    top_col1, top_col2 = st.columns([1.2, 3])
    with top_col1:
        standard = st.selectbox(
            "选择标准",
            options=[
                "GB/T 1800.1-2020 极限与配合基础",
                "GB/T 1800.2-2020 极限偏差表",
                "GB/T 1801-2009 极限与配合配合制",
                "GB/T 1182-2018 几何公差标注",
                "GB/T 17851-2010 基准和基准体系",
                "GB/T 4249-2009 公差原则",
                "GB/T 45683-2025 一般几何规范"
            ],
            index=0,
            key="std_ref_select"
        )

    with top_col2:
        # 阅读模式：目录浏览 / 原文阅读
        view_mode = st.radio(
            "阅读模式",
            ["📖 目录浏览", "📄 原文阅读"],
            horizontal=True,
            index=0,
            key="std_view_mode"
        )

    # 提取当前标准简称
    current_standard = None
    if "GB/T 1800.1-2020" in standard:
        current_standard = "GB/T 1800.1-2020"
    elif "GB/T 1800.2-2020" in standard:
        current_standard = "GB/T 1800.2-2020"
    elif "GB/T 1801-2009" in standard:
        current_standard = "GB/T 1801-2009"
    elif "GB/T 1182-2018" in standard:
        current_standard = "GB/T 1182-2018"
    elif "GB/T 17851-2010" in standard:
        current_standard = "GB/T 17851-2010"
    elif "GB/T 4249-2009" in standard:
        current_standard = "GB/T 4249-2009"
    elif "GB/T 45683-2025" in standard:
        current_standard = "GB/T 45683-2025"

    # ==================== 原文阅读模式 ====================
    if "原文阅读" in view_mode:
        if "GB/T 1800.1-2020" in standard:
            render_gbt1800_fulltext()
        elif "GB/T 1800.2-2020" in standard:
            render_gbt18002_fulltext()
        elif "GB/T 1801-2009" in standard:
            render_gbt1801_fulltext()
        elif "GB/T 1182-2018" in standard:
            render_gbt1182_fulltext()
        elif "GB/T 17851-2010" in standard:
            render_gbt17851_fulltext()
        elif "GB/T 4249-2009" in standard:
            render_gbt4249_fulltext()
        elif "GB/T 45683-2025" in standard:
            render_gbt45683_fulltext()
        return

    # ==================== 目录浏览模式（原有搜索功能） ====================

    search_col1, search_col2, search_col3 = st.columns([1.2, 2.5, 0.8])
    with search_col1:
        pass  # 标准已在上面选择

    with search_col2:
        search_query = st.text_input(
            "🔍 搜索关键词",
            placeholder="输入关键词如：IT7、H7、f6、圆度、同轴度、间隙配合...",
            key="std_ref_search"
        )

    with search_col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        search_clicked = st.button("🔎 搜索", type="primary", use_container_width=True, key="std_ref_search_btn")

    # 执行搜索
    search_results = []
    if search_clicked and search_query:
        search_results = _search_glossary(glossary, search_query, current_standard)

    # 显示搜索结果
    if search_clicked:
        st.markdown("---")
        if not search_query:
            st.warning("⚠️ 请输入搜索关键词")
        elif not search_results:
            st.warning(f"⚠️ 未在 **{standard}** 中找到与「{search_query}」相关的内容")
            st.info("💡 提示：可尝试其他关键词，如 IT7、H7、f6、圆度、同轴度、间隙配合、基准孔 等")
        else:
            st.success(f"✅ 找到 **{len(search_results)}** 条与「{search_query}」相关的结果")
            # 显示术语解释卡片
            for i, result in enumerate(search_results):
                match_badge = "🎯" if result["match_type"] == "精确匹配" else "📌"
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin-bottom: 12px; background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);">
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 20px; font-weight: bold; color: #1a73e8;">{result['term']}</span>
                            <span style="margin-left: 10px; font-size: 12px; background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 12px;">{match_badge} {result['match_type']}</span>
                            <span style="margin-left: 8px; font-size: 12px; background: #e6f4ea; color: #137333; padding: 2px 8px; border-radius: 12px;">📍 {result['location']}</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="font-weight: bold; color: #5f6368;">📖 术语解释：</span>
                            <span style="color: #333;">{result['explain']}</span>
                        </div>
                        <div>
                            <span style="font-weight: bold; color: #5f6368;">📄 标准含义：</span>
                            <span style="color: #333;">{result['doc_meaning']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")

    # 根据选择的标准显示内容，搜索后自动展开匹配的 expander
    if "GB/T 1800.1-2020" in standard:
        render_gbt1800_content(search_query, search_results if search_clicked else [])
    elif "GB/T 1800.2-2020" in standard:
        render_gbt18002_content(search_query, search_results if search_clicked else [])
    elif "GB/T 1801-2009" in standard:
        render_gbt1801_content(search_query, search_results if search_clicked else [])
    elif "GB/T 1182-2018" in standard:
        render_gbt1182_content(search_query, search_results if search_clicked else [])
    elif "GB/T 17851-2010" in standard:
        render_gbt17851_content(search_query, search_results if search_clicked else [])
    elif "GB/T 4249-2009" in standard:
        render_gbt4249_content(search_query, search_results if search_clicked else [])
    elif "GB/T 45683-2025" in standard:
        render_gbt45683_content(search_query, search_results if search_clicked else [])


def render_gbt1800_content(search_query, search_results):
    """显示 GB/T 1800.1-2020 标准内容"""
    st.markdown("### 📖 GB/T 1800.1-2020 极限与配合 基础")

    # 标准信息
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 极限与配合 第1部分：公差、偏差和配合的基础  
    **适用范围**：圆柱表面及其他表面或结构的尺寸要素
    """)

    # 判断哪些 expander 需要展开（基于搜索结果定位）
    matched_locations = set()
    if search_results:
        for r in search_results:
            matched_locations.add(r["location"])

    # 标准公差等级表
    expand_it = "标准公差数值表" in " ".join(matched_locations)
    with st.expander("📊 标准公差数值表 (IT01-IT18)", expanded=expand_it):
        size_labels = [f"{r[0]}-{r[1]}" for r in SIZE_RANGES]
        it_grades_list = ["IT5", "IT6", "IT7", "IT8", "IT9", "IT10", "IT11", "IT12"]

        df_data = {"尺寸分段(mm)": size_labels}
        for grade in it_grades_list:
            df_data[grade] = IT_VALUES[grade]

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 如果搜索了具体IT等级，高亮显示
        if search_results:
            for r in search_results:
                if r["term"].startswith("IT") and r["term"] in IT_VALUES:
                    vals = IT_VALUES[r["term"]]
                    st.markdown(f"📌 **{r['term']}**：公差值范围 {min(vals)} ~ {max(vals)} μm")

    # 基本偏差说明
    expand_dev = "基本偏差" in " ".join(matched_locations)
    with st.expander("📐 基本偏差系列", expanded=expand_dev):
        st.markdown("""
        **孔的基本偏差（A-ZC）**：
        - A-H：下偏差 EI（正值，间隙配合）
        - J-N：过渡配合
        - P-ZC：过盈配合
        - H：基准孔，EI = 0

        **轴的基本偏差（a-zc）**：
        - a-h：上偏差 es（负值，间隙配合）
        - j-n：过渡配合
        - p-zc：过盈配合
        - h：基准轴，es = 0
        """)

        # 显示匹配的基本偏差
        if search_results:
            for r in search_results:
                if len(r["term"]) == 1 and r["term"].isalpha():
                    st.markdown(f"📌 **{r['term']}**：{r['explain']}")

    # 配合类型说明
    expand_fit = "配合类型" in " ".join(matched_locations)
    with st.expander("🔗 配合类型", expanded=expand_fit):
        st.markdown("""
        | 配合类型 | 条件 | 特性 |
        |---------|------|------|
        | 间隙配合 | 孔最小 ≥ 轴最大 | 可相对运动 |
        | 过渡配合 | 可能有间隙或过盈 | 精确定位 |
        | 过盈配合 | 孔最大 ≤ 轴最小 | 固定连接 |
        """)

        if search_results:
            for r in search_results:
                if r["term"] in ["间隙配合", "过渡配合", "过盈配合"]:
                    st.markdown(f"📌 **{r['term']}**：{r['doc_meaning']}")


def render_gbt1801_content(search_query, search_results):
    """显示 GB/T 1801-2009 标准内容"""
    st.markdown("### 📖 GB/T 1801-2009 极限与配合配合制")

    st.info("""
    **标准名称**：产品几何技术规范(GPS) 极限与配合 公差带和配合的选择  
    **适用范围**：光滑圆柱表面及单一尺寸要素的配合选择
    """)

    matched_locations = set()
    if search_results:
        for r in search_results:
            matched_locations.add(r["location"])

    # 常用配合表
    expand_common = "常用配合" in " ".join(matched_locations)
    with st.expander("📋 常用配合代号", expanded=expand_common):
        fit_data = []
        for fit_name, fit_info in COMMON_FITS_INFO.items():
            fit_data.append({
                "配合代号": fit_name,
                "配合类型": fit_info["type"],
                "说明": fit_info["description"][:40] + "..." if len(fit_info["description"]) > 40 else fit_info["description"]
            })

        df_fits = pd.DataFrame(fit_data)
        st.dataframe(df_fits, use_container_width=True, hide_index=True)

        # 显示匹配的配合
        if search_results:
            matched_fits = [r for r in search_results if r["term"] in COMMON_FITS_INFO]
            if matched_fits:
                st.markdown("---")
                st.markdown("**📌 匹配的配合说明：**")
                for r in matched_fits:
                    st.markdown(f"- **{r['term']}**（{r['match_type']}）：{r['explain']}")

    # 优先配合
    expand_priority = "优先配合" in " ".join(matched_locations)
    with st.expander("⭐ 优先配合推荐", expanded=expand_priority):
        st.markdown("""
        **基孔制优先配合**：
        - H11/c11, H9/d9, H8/f7, H7/f6, H7/g6, H7/h6
        - H7/k6, H7/n6, H7/p6, H7/s6

        **基轴制优先配合**：
        - C11/h11, D9/h9, F8/h7, F7/h6, G7/h6, H7/h6
        - K7/h6, N7/h6, P7/h6, S7/h6
        """)

        if search_results:
            for r in search_results:
                if r["term"] in ["优先配合", "基孔制", "基轴制"]:
                    st.markdown(f"📌 **{r['term']}**：{r['doc_meaning']}")


def render_gbt1182_content(search_query, search_results):
    """显示 GB/T 1182-2018 标准内容"""
    st.markdown("### 📖 GB/T 1182-2018 产品几何技术规范(GPS) 几何公差")

    st.info("""
    **标准名称**：产品几何技术规范(GPS) 几何公差 形状、方向、位置和跳动公差标注  
    **适用范围**：机械零件的几何公差（形状、方向、位置和跳动公差）标注
    **发布日期**：2018-05-14 | **实施日期**：2018-12-01
    **代替**：GB/T 1182-2008
    """)

    matched_locations = set()
    if search_results:
        for r in search_results:
            matched_locations.add(r["location"])

    # 形位公差项目
    expand_gdandt = "形位公差项目" in " ".join(matched_locations)
    with st.expander("📐 形位公差项目及符号", expanded=expand_gdandt):
        gdandt_items = [
            {"项目": "直线度", "符号": "—", "类型": "形状公差", "有基准": "否"},
            {"项目": "平面度", "符号": "▱", "类型": "形状公差", "有基准": "否"},
            {"项目": "圆度", "符号": "○", "类型": "形状公差", "有基准": "否"},
            {"项目": "圆柱度", "符号": "⌭", "类型": "形状公差", "有基准": "否"},
            {"项目": "平行度", "符号": "∥", "类型": "方向公差", "有基准": "是"},
            {"项目": "垂直度", "符号": "⊥", "类型": "方向公差", "有基准": "是"},
            {"项目": "倾斜度", "符号": "∠", "类型": "方向公差", "有基准": "是"},
            {"项目": "同轴度", "符号": "◎", "类型": "位置公差", "有基准": "是"},
            {"项目": "对称度", "符号": "⌢", "类型": "位置公差", "有基准": "是"},
            {"项目": "位置度", "符号": "⌖", "类型": "位置公差", "有基准": "是"},
            {"项目": "圆跳动", "符号": "↗", "类型": "跳动公差", "有基准": "是"},
            {"项目": "全跳动", "符号": "⇗", "类型": "跳动公差", "有基准": "是"},
        ]

        df_gdandt = pd.DataFrame(gdandt_items)
        st.dataframe(df_gdandt, use_container_width=True, hide_index=True)

        # 显示匹配的形位公差
        if search_results:
            gdandt_names = [item["项目"] for item in gdandt_items]
            matched_gdandt = [r for r in search_results if r["term"] in gdandt_names]
            if matched_gdandt:
                st.markdown("---")
                st.markdown("**📌 匹配的形位公差说明：**")
                for r in matched_gdandt:
                    st.markdown(f"- **{r['term']}**（{r['match_type']}）：{r['explain']}")

    # 公差等级
    expand_grade = "形位公差等级" in " ".join(matched_locations)
    with st.expander("📊 形位公差等级", expanded=expand_grade):
        st.markdown("""
        **公差等级**：1~12级（1级最高，12级最低）

        **常用等级范围**：
        - 圆度、圆柱度：0~12级
        - 直线度、平面度：1~12级
        - 平行度、垂直度：1~12级
        - 同轴度、对称度：1~12级
        - 圆跳动、全跳动：1~12级
        """)

    # 未注公差
    expand_untol = "未注公差" in " ".join(matched_locations)
    with st.expander("📝 未注公差值", expanded=expand_untol):
        st.markdown("""
        **未注公差等级**：H（精密）、K（中等）、L（粗糙）

        当图样上未标注形位公差时，按以下标准执行：
        - 直线度/平面度：按 GB/T 1184-H/K/L
        - 垂直度：按 GB/T 1184-H/K/L
        - 对称度：按 GB/T 1184-H/K/L
        - 圆跳动：按 GB/T 1184-H/K/L
        """)

        if search_results:
            for r in search_results:
                if r["term"] == "未注公差":
                    st.markdown(f"📌 **{r['term']}**：{r['doc_meaning']}")


# ============================================================
# 第11节：国家标准原文阅读
# ============================================================

def render_gbt1800_fulltext():
    """GB/T 1800.1-2020 原文阅读"""
    st.markdown("### 📖 GB/T 1800.1-2020 原文")
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 线性尺寸公差ISO代号体系 第1部分：公差、偏差和配合的基础  
    **发布日期**：2020-12-14 | **实施日期**：2021-07-01 | **代替**：GB/T 1800.1-2009, GB/T 1801-2009  
    **ICS分类**：17.040.10 | **中国标准分类号**：J04
    """)

    # 目录导航
    with st.expander("📑 本标准章节目录", expanded=True):
        chapters = [
            ("第1章", "范围"),
            ("第2章", "规范性引用文件"),
            ("第3章", "术语和定义"),
            ("第4章", "概述"),
            ("第5章", "公差"),
            ("第6章", "偏差"),
            ("第7章", "配合"),
            ("第8章", "公差带代号"),
            ("第9章", "代号体系"),
            ("第10章", "标注"),
        ]
        for ch, title in chapters:
            st.write(f"**{ch}** {title}")

    # 第1章 范围
    with st.expander("📗 第1章 范围", expanded=False):
        st.markdown("""
        **1.1 概述**

        GB/T 1800的本部分建立了线性尺寸公差的ISO代号体系，适用于以下类型的尺寸要素：

        a) 圆柱表面；

        b) 两相对平行平面。

        **1.2 目的**

        本部分的主要目的是：

        a) 为线性尺寸公差建立ISO代号体系；

        b) 定义线性尺寸公差ISO代号体系的基本概念和相关术语；

        c) 提供选择公差带代号的标准化方法。
        """)

    # 第2章 规范性引用文件
    with st.expander("📗 第2章 规范性引用文件", expanded=False):
        st.markdown("""
        下列文件中的条款通过GB/T 1800的本部分的引用而成为本部分的条款：

        - GB/T 1800.2-2009 产品几何技术规范(GPS) 极限与配合 第2部分：标准公差等级和孔、轴极限偏差表

        - GB/T 1801-2009 产品几何技术规范(GPS) 极限与配合 公差带和配合的选择

        - ISO 1:1975 产品几何技术规范(GPS) 标准化参考温度及标准测量温度
        """)

    # 第3章 术语和定义
    with st.expander("📗 第3章 术语和定义", expanded=True):
        st.markdown("""
        **3.1 尺寸**

        **3.1.1 尺寸（线性尺寸）**：以特定单位表示线性尺寸的数值。

        **3.1.2 公称尺寸**：设计给定的尺寸。

        **3.1.3 极限尺寸**：一个尺寸界限的两个尺寸之一。

        **3.1.4 最大极限尺寸**：允许的最大尺寸。

        **3.1.5 最小极限尺寸**：允许的最小尺寸。

        ---

        **3.2 偏差**

        **3.2.1 偏差**：某一尺寸减其公称尺寸所得的代数差。

        **3.2.2 上偏差**：最大极限尺寸减其公称尺寸所得的代数差。

        **3.2.3 下偏差**：最小极限尺寸减其公称尺寸所得的代数差。

        ---

        **3.3 公差**

        **3.3.1 公差**：最大极限尺寸减最小极限尺寸之差，或上偏差减下偏差之差。它是允许的误差范围。

        **3.3.2 标准公差（IT）**：国家标准规定的公差值，用IT表示。

        **3.3.3 公差等级**：确定尺寸精确程度的等级。代号：IT01, IT0, IT1, IT2, … IT18。

        ---

        **3.4 配合**

        **3.4.1 配合**：基本尺寸相同的、相互结合的孔和轴公差带之间的关系。

        **3.4.2 配合制**：同一极限制的孔和轴组成配合的一种制度。

        ---

        **3.5 公差带**

        **3.5.1 公差带**：由上偏差和下偏差或最大极限尺寸和最小极限尺寸所限定的区域。

        **3.5.2 基本偏差**：用于确定公差带相对于零线位置的极限偏差。

        ---

        **3.6 配合类型**

        **3.6.1 间隙配合**：具有间隙（含最小间隙等于零）的配合。孔的最小极限尺寸大于或等于轴的最大极限尺寸。

        **3.6.2 过盈配合**：具有过盈（含最小过盈等于零）的配合。孔的最大极限尺寸小于或等于轴的最小极限尺寸。

        **3.6.3 过渡配合**：可能具有间隙或过盈的配合。孔的最大极限尺寸大于轴的最小极限尺寸，且孔的最小极限尺寸小于轴的最大极限尺寸。
        """)

    # 第4章 概述
    with st.expander("📗 第4章 概述", expanded=False):
        st.markdown("""
        **4.1 线性尺寸公差代号体系**

        线性尺寸公差的代号体系基于：

        - 公称尺寸分段（见GB/T 1800.2-2009表1）

        - 标准公差等级（IT01至IT18）

        - 基本偏差代号（孔用大写字母A至ZC，轴用小写字母a至zc）

        **4.2 公差带代号**

        公差带代号由基本偏差代号和公差等级数字组成。

        示例：

        - H7：基本偏差为H，公差等级为IT7的孔公差带

        - h6：基本偏差为h，公差等级为IT6的轴公差带

        - F7：基本偏差为F，公差等级为IT7的孔公差带

        **4.3 配合代号**

        配合代号由孔公差带代号和轴公差带代号组成，中间用斜线"/"分隔。

        示例：H7/f6（基孔制间隙配合）、H7/p6（基孔制过盈配合）
        """)

    # 第5章 公差
    with st.expander("📗 第5章 公差", expanded=False):
        st.markdown("""
        **5.1 标准公差等级**

        标准公差等级分为：IT01, IT0, IT1, IT2, IT3, IT4, IT5, IT6, IT7, IT8, IT9, IT10, IT11, IT12, IT13, IT14, IT15, IT16, IT17, IT18。

        **5.2 标准公差值**

        标准公差值由公称尺寸所在的尺寸分段和公差等级共同决定。

        **5.3 公差等级的应用**

        - **IT01, IT0, IT1**：用于特别精密的量块、量规等

        - **IT2 ~ IT4**：用于精密配合

        - **IT5 ~ IT7**：用于一般精密配合，是机械制造中最重要的公差等级

        - **IT8 ~ IT12**：用于一般用途的配合和非配合尺寸

        - **IT13 ~ IT18**：用于未注公差尺寸
        """)

    # 第6章 偏差
    with st.expander("📗 第6章 偏差", expanded=False):
        st.markdown("""
        **6.1 基本偏差**

        基本偏差是确定公差带相对于零线位置的极限偏差。

        **6.2 孔的基本偏差（A ~ ZC）**

        | 代号范围 | 偏差性质 | 配合类型 |
        |---------|---------|---------|
        | A ~ H | 下偏差EI为正值或零 | 间隙配合 |
        | J ~ N | 偏差值较小 | 过渡配合 |
        | P ~ ZC | 下偏差EI为负值 | 过盈配合 |

        **基准孔H**：下偏差EI = 0

        **6.3 轴的基本偏差（a ~ zc）**

        | 代号范围 | 偏差性质 | 配合类型 |
        |---------|---------|---------|
        | a ~ h | 上偏差es为负值或零 | 间隙配合 |
        | j ~ n | 偏差值较小 | 过渡配合 |
        | p ~ zc | 上偏差es为正值 | 过盈配合 |

        **基准轴h**：上偏差es = 0

        **6.4 偏差值表**

        孔和轴的基本偏差数值见GB/T 1800.2-2009。
        """)

    # 第7章 配合
    with st.expander("📗 第7章 配合", expanded=False):
        st.markdown("""
        **7.1 配合制**

        **7.1.1 基孔制配合**

        基孔制配合是指孔的基本偏差不变（通常为H），通过改变轴的基本偏差来得到不同性质的配合。

        特点：加工孔通常需要定值刀具（如钻头、铰刀），因此优先采用基孔制以减少刀具规格。

        **7.1.2 基轴制配合**

        基轴制配合是指轴的基本偏差不变（通常为h），通过改变孔的基本偏差来得到不同性质的配合。

        适用情况：

        - 同一轴上装有不同配合要求的零件时（如活塞销）

        - 采用冷拉圆钢作轴不再加工时

        - 标准件外径（如滚动轴承外圈）与箱体孔配合时

        **7.2 配合类型**

        **间隙配合**：孔与轴之间有间隙，可相对运动。特征：孔的最小极限尺寸 ≥ 轴的最大极限尺寸。

        **过渡配合**：孔与轴之间可能为间隙也可能为过盈。特征：孔的最大极限尺寸 > 轴的最小极限尺寸，且孔的最小极限尺寸 < 轴的最大极限尺寸。

        **过盈配合**：孔与轴之间有过盈，不可相对运动。特征：孔的最大极限尺寸 ≤ 轴的最小极限尺寸。

        **7.3 配合的选择**

        配合的选择应综合考虑：

        - 工件的工作条件（运动精度、承载能力、装拆要求等）

        - 加工工艺和成本

        - 标准化和互换性要求

        优先选用优先配合。
        """)

    # 第8章 公差带代号
    with st.expander("📗 第8章 公差带代号", expanded=False):
        st.markdown("""
        **8.1 孔公差带代号**

        孔的公差带代号由基本偏差代号（大写字母）和公差等级数字组成。

        GB/T 1800.2-2009 规定了孔的常用公差带：

        - IT5：G5, H5, Js5, K5, M5, N5, P5, R5, S5, T5

        - IT6：C6, D6, E6, F6, G6, H6, Js6, K6, M6, N6, P6, R6, S6, T6, U6

        - IT7：D7, E7, F7, G7, H7, Js7, K7, M7, N7, P7, R7, S7, T7, U7

        - IT8：C8, D8, E8, F8, G8, H8, Js8, K8, M8, N8

        - IT9：C9, D9, E9, F9, G9, H9

        - IT10：C10, D10, E10, F10, H10

        - IT11：B11, C11, D11, H11

        - IT12：A12, B12, H12

        **8.2 轴公差带代号**

        轴的公差带代号由基本偏差代号（小写字母）和公差等级数字组成。

        GB/T 1800.2-2009 规定了轴的常用公差带，结构与孔类似。

        **8.3 公差带的选择原则**

        - 优先选用基本偏差H（孔）或h（轴）作为基准

        - 优先选用常用公差带中的公差带

        - 尽量减少公差带种类的数量
        """)

    # 第9章 代号体系
    with st.expander("📗 第9章 代号体系", expanded=False):
        st.markdown("""
        **9.1 配合代号表示方法**

        配合代号由孔公差带代号、斜线"/"和轴公差带代号组成。

        格式：**孔公差带代号 / 轴公差带代号**

        示例：H7/f6, F7/h6, H7/p6, K7/h6

        **9.2 基孔制与基轴制的表示**

        基孔制配合示例：H7/f6, H7/g6, H7/h6, H7/k6, H7/n6, H7/p6, H7/s6

        基轴制配合示例：F7/h6, G7/h6, H7/h6, K7/h6, N7/h6, P7/h6, S7/h6

        **9.3 优先配合**

        GB/T 1801-2009 规定了13种基孔制优先配合和13种基轴制优先配合。

        设计时应优先选用这些配合。
        """)

    # 第10章 标注
    with st.expander("📗 第10章 标注", expanded=False):
        st.markdown("""
        **10.1 公称尺寸标注**

        在图样上，公称尺寸以毫米为单位，用数字表示。

        示例：ø50, 80, 120

        **10.2 公差带代号标注**

        在公称尺寸后标注公差带代号。

        示例：ø50H7, 80g6, 120JS8

        **10.3 配合代号标注**

        在公称尺寸后标注配合代号。

        示例：ø50H7/g6, 80H7/h6, 120F8/h7

        **10.4 极限偏差标注**

        也可以在公称尺寸后标注极限偏差值。

        示例：ø50^+0.025, 80_{-0.025}^{-0.010}, 120±0.035

        **10.5 标注位置**

        公称尺寸和公差代号应标注在可见轮廓线、引出线或尺寸界线的旁边。

        线性尺寸的数字应按水平方向书写。
        """)


def render_gbt1801_fulltext():
    """GB/T 1801-2009 原文阅读"""
    st.markdown("### 📖 GB/T 1801-2009 原文")
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 极限与配合 公差带和配合的选择  
    **发布日期**：2009-05-06 | **实施日期**：2009-11-01 | **代替**：GB/T 1801-1999  
    **ICS分类**：17.040.10 | **中国标准分类号**：J04  
    **与ISO标准的对应关系**：ISO 1829:1975（NEQ，非等效）
    """)

    # 目录
    with st.expander("📑 本标准章节目录", expanded=True):
        chapters = [
            ("第1章", "范围"),
            ("第2章", "规范性引用文件"),
            ("第3章", "术语和定义"),
            ("第4章", "总则"),
            ("第5章", "公差带的选择"),
            ("第6章", "配合的选择"),
            ("第7章", "配合的应用"),
            ("附录A", "常用配合"),
            ("附录B", "配合选择说明"),
        ]
        for ch, title in chapters:
            st.write(f"**{ch}** {title}")

    # 第1章 范围
    with st.expander("📗 第1章 范围", expanded=False):
        st.markdown("""
        **1.1 概述**

        GB/T 1801的本部分规定了公差带和配合的选择原则，适用于光滑圆柱表面及单一尺寸要素的公差带和配合的选择。

        **1.2 适用范围**

        - 光滑圆柱表面

        - 单一尺寸要素（指单一厚度或宽度）

        - 公称尺寸至5000mm

        **1.3 不适用范围**

        - 特殊场合下的配合

        - 其他几何要素的配合

        - 已由其他国家标准规定的场合
        """)

    # 第2章 规范性引用文件
    with st.expander("📗 第2章 规范性引用文件", expanded=False):
        st.markdown("""
        下列文件中的条款通过GB/T 1801的本部分的引用而成为本部分的条款：

        - GB/T 1800.1-2009 产品几何技术规范(GPS) 极限与配合 第1部分：公差、偏差和配合的基础

        - GB/T 1800.2-2009 产品几何技术规范(GPS) 极限与配合 第2部分：标准公差等级和孔、轴极限偏差表

        - GB/T 4458.5-2003 机械制图 尺寸注法
        """)

    # 第3章 术语和定义
    with st.expander("📗 第3章 术语和定义", expanded=True):
        st.markdown("""
        **3.1 配合制**

        **3.1.1 基孔制配合**：基本偏差为一定的孔的公差带，与不同基本偏差的轴的公差带形成各种配合的制度。基准孔代号为H。

        **3.1.2 基轴制配合**：基本偏差为一定的轴的公差带，与不同基本偏差的孔的公差带形成各种配合的制度。基准轴代号为h。

        **3.2 配合类型**

        **3.2.1 间隙配合**：具有间隙（含最小间隙等于零）的配合。

        **3.2.2 过渡配合**：可能具有间隙或过盈的配合。

        **3.2.3 过盈配合**：具有过盈（含最小过盈等于零）的配合。

        **3.3 配合选择**

        **3.3.1 优先配合**：在一般机械制造中优先选用的配合。

        **3.3.2 常用配合**：在优先配合的基础上扩展的一般用途配合。
        """)

    # 第4章 总则
    with st.expander("📗 第4章 总则", expanded=False):
        st.markdown("""
        **4.1 配合选择的一般原则**

        配合的选择应综合考虑以下因素：

        1. **工作条件**：包括运动精度、承载能力、转速、润滑条件、工作温度等

        2. **装配要求**：包括装拆的频繁程度、定位精度要求等

        3. **工艺性**：考虑加工和检测的可行性

        4. **经济性**：在满足使用要求的前提下，降低加工成本

        5. **标准化**：优先选用标准规定的配合

        **4.2 选择顺序**

        配合的选择应按以下顺序进行：

        1. 首先考虑选用优先配合

        2. 其次选用常用配合

        3. 最后考虑特殊配合（必要时）

        **4.3 配合制的选择**

        - 一般情况下，优先采用基孔制

        - 当有合理理由时，可采用基轴制

        - 应使孔和轴的加工工艺等价
        """)

    # 第5章 公差带的选择
    with st.expander("📗 第5章 公差带的选择", expanded=False):
        st.markdown("""
        **5.1 孔公差带**

        GB/T 1800.2-2009 规定了105种孔的常用公差带。

        主要公差等级及代号示例：

        | 公差等级 | 常用孔公差带 |
        |---------|------------|
        | IT5 | G5, H5, Js5, K5, M5, N5 |
        | IT6 | C6, D6, E6, F6, G6, H6, Js6, K6, M6, N6, P6, R6, S6, T6, U6 |
        | IT7 | D7, E7, F7, G7, H7, Js7, K7, M7, N7, P7, R7, S7, T7, U7 |
        | IT8 | C8, D8, E8, F8, G8, H8, Js8, K8, M8, N8 |
        | IT9 | C9, D9, E9, F9, G9, H9 |
        | IT10 | C10, D10, E10, F10, H10 |
        | IT11 | B11, C11, D11, H11 |
        | IT12 | A12, B12, H12 |

        **5.2 轴公差带**

        GB/T 1800.2-2009 规定了105种轴的常用公差带。

        结构与孔类似，小写字母表示基本偏差。

        **5.3 公差带选择原则**

        - 一般用途选择常用公差带

        - 精密仪器、仪表可选择较高等级的公差带

        - 粗加工、自由公差可选择较低等级的公差带
        """)

    # 第6章 配合的选择
    with st.expander("📗 第6章 配合的选择", expanded=False):
        st.markdown("""
        **6.1 基孔制优先配合**

        | 配合类型 | 优先配合代号 | 说明 |
        |---------|------------|------|
        | 间隙配合 | H6/g5, H7/f6, H8/f7, H9/d9, H11/c11 | 用于相对运动或有间隙要求的场合 |
        | 过渡配合 | H7/k6, H7/js6 | 用于定位准确、可拆装的场合 |
        | 过盈配合 | H7/p6, H7/r6, H7/s6, H7/u6 | 用于传递扭矩或固定连接的场合 |

        **6.2 基轴制优先配合**

        | 配合类型 | 优先配合代号 | 说明 |
        |---------|------------|------|
        | 间隙配合 | F6/h5, F7/h6, F8/h7, D9/h9, C11/h11 | 用于相对运动的场合 |
        | 过渡配合 | K6/h5, K7/h6, Js7/h6 | 用于定位准确的场合 |
        | 过盈配合 | P6/h5, P7/h6, S6/h5, S7/h6, U7/h6 | 用于传递扭矩的场合 |

        **6.3 配合选择的考虑因素**

        **间隙配合的选择因素：**

        - 运动精度要求（转速、润滑条件）

        - 最小间隙要求

        - 导向精度要求

        **过渡配合的选择因素：**

        - 对中精度要求

        - 装拆频次

        - 定位可靠性要求

        **过盈配合的选择因素：**

        - 扭矩传递要求

        - 装配方法（压入、热装、冷缩）

        - 连接强度要求
        """)

    # 第7章 配合的应用
    with st.expander("📗 第7章 配合的应用", expanded=False):
        st.markdown("""
        **7.1 间隙配合的应用**

        | 配合代号 | 应用举例 |
        |---------|---------|
        | H11/c11 | 粗糙联接，如垫圈、夹铁 |
        | H9/d9 | 粗糙滑动配合，如开式齿轮、皮带轮与轴 |
        | H8/f7 | 滑动配合，如滑块、活塞与气缸 |
        | H7/f6 | 精密滑动配合，如车床尾座套筒 |
        | H7/g6 | 精确定位配合，如钻模与钻套 |
        | H6/g5 | 精密仪器中的滑动件 |

        **7.2 过渡配合的应用**

        | 配合代号 | 应用举例 |
        |---------|---------|
        | H7/js6 | 易于拆卸的定位配合，如齿轮、皮带轮与轴 |
        | H7/k6 | 常用过渡配合，如联轴器与轴 |
        | H7/n6 | 较紧的过渡配合，如蜗轮与青铜轮毂 |

        **7.3 过盈配合的应用**

        | 配合代号 | 应用举例 |
        |---------|---------|
        | H7/p6 | 轻过盈配合，需要键或销传递扭矩 |
        | H7/r6 | 中等过盈配合，可少量键传递扭矩 |
        | H7/s6 | 重要过盈配合，需加热或冷却装配 |
        | H7/u6 | 重过盈配合，用于重大载荷连接 |

        **7.4 配合选择实例**

        **例1：减速器齿轮与轴的配合**

        - 传递较大扭矩，需要定位可靠

        - 选用H7/k6或H7/m6过渡配合

        **例2：滑动轴承与箱体孔的配合**

        - 需要轴在孔中滑动

        - 选用H7/f6或H8/f7间隙配合

        **例3：火车轮与轴的配合**

        - 传递很大扭矩

        - 选用H7/u6或更紧的过盈配合
        """)

    # 附录A
    with st.expander("📗 附录A 常用配合", expanded=False):
        st.markdown("""
        **A.1 基孔制常用配合**

        GB/T 1801-2009 规定了基孔制常用配合共59种。

        **A.2 基轴制常用配合**

        GB/T 1801-2009 规定了基轴制常用配合共47种。

        **A.3 常用配合表**

        | 公称尺寸mm | 配合代号 | 配合类型 |
        |-----------|---------|---------|
        | ≤3 | H6/g5, H7/h6, H7/k6, H7/n6, H7/p6 | 间隙~过盈 |
        | 3~6 | H7/f6, H7/g6, H7/h6, H7/k6, H7/m6, H7/n6, H7/p6, H7/s6 | 间隙~过盈 |
        | 6~10 | H7/f6, H7/g6, H7/h6, H7/js6, H7/k6, H7/m6, H7/n6, H7/p6, H7/r6, H7/s6 | 间隙~过盈 |
        | 10~18 | H7/f6, H7/g6, H7/h6, H7/js6, H7/k6, H7/m6, H7/n6, H7/p6, H7/r6, H7/s6 | 间隙~过盈 |
        | 18~30 | H7/f6, H7/g6, H7/h6, H7/js6, H7/k6, H7/m6, H7/n6, H7/p6, H7/r6, H7/s6, H7/u6 | 间隙~过盈 |
        | 30~50 | H7/f6, H7/g6, H7/h6, H7/js6, H7/k6, H7/m6, H7/n6, H7/p6, H7/r6, H7/s6, H7/u6 | 间隙~过盈 |
        | 50~80 | H7/f6, H7/g6, H7/h6, H7/js6, H7/k6, H7/m6, H7/n6, H7/p6, H7/r6, H7/s6, H7/t6, H7/u6 | 间隙~过盈 |

        更多尺寸分段的配合表见GB/T 1800.2-2009。
        """)

    # 附录B
    with st.expander("📗 附录B 配合选择说明", expanded=False):
        st.markdown("""
        **B.1 配合选择的原则说明**

        1. **满足功能要求**：配合的选择应首先满足零件的功能要求，如运动精度、承载能力等。

        2. **考虑工艺经济性**：在满足功能要求的前提下，应选择加工工艺性好、成本低的配合。

        3. **保持一致性**：同类零件应采用相同的配合制度，便于生产管理。

        **B.2 配合公差带的应用指南**

        **间隙配合的应用指南：**

        - 最小间隙为零时，选用H/h配合

        - 需补偿变形误差时，选用H/g配合

        - 要求精确对中时，选用H/f配合

        **过渡配合的应用指南：**

        - 需经常拆卸时，选用H/js或H/k配合

        - 要求定位准确时，选用H/k或H/m配合

        - 不常拆卸且要求连接牢固时，选用H/n配合

        **过盈配合的应用指南：**

        - 可用手推入装配时，选用H/p或H/r配合

        - 需锤击或压力机装配时，选用H/s配合

        - 需加热或冷却装配时，选用H/t或H/u配合
        """)


def render_gbt1182_fulltext():
    """GB/T 1182-2018 原文阅读"""
    st.markdown("### 📖 GB/T 1182-2018 原文")
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 几何公差 形状、方向、位置和跳动公差标注  
    **发布日期**：2018-05-14 | **实施日期**：2018-12-01 | **代替**：GB/T 1182-2008  
    **ICS分类**：17.040.10 | **中国标准分类号**：J04  
    **与ISO标准的对应关系**：ISO 1101:2017（MOD，修改采用）
    """)

    # 目录
    with st.expander("📑 本标准章节目录", expanded=True):
        chapters = [
            ("第1章", "适用范围"),
            ("第2章", "引用标准"),
            ("第3章", "定义"),
            ("第4章", "总则"),
            ("第5章", "形状和位置公差的未注公差值"),
            ("第6章", "图样上的表示法"),
            ("第7章", "特殊情况"),
            ("附录A", "未注公差值的解释"),
            ("附录B", "形位公差注出公差值"),
        ]
        for ch, title in chapters:
            st.write(f"**{ch}** {title}")

    # 第1章 适用范围
    with st.expander("📗 第1章 适用范围", expanded=False):
        st.markdown("""
        **1.1 概述**

        本标准主要适用于用去除材料方法形成的要素，也可用于其他方法形成的要素。

        **1.2 适用要素**

        本标准适用于以下几何特征：

        - 直线度

        - 平面度

        - 圆度

        - 圆柱度

        - 平行度

        - 垂直度

        - 同轴度

        - 对称度

        - 圆跳动

        - 全跳动

        **1.3 使用条件**

        使用时应确定本部门的制造精度是否与本标准规定的公差等级相适应。
        """)

    # 第2章 引用标准
    with st.expander("📗 第2章 引用标准", expanded=False):
        st.markdown("""
        下列标准所包含的条文，通过在本标准中引用而构成为本标准的条文：

        - GB/T 1182-1996 形状和位置公差 通则、定义、符号和图样表示法

        - GB/T 1958-1980 形状和位置公差 检测规定

        - ISO 2768-1:1989 一般几何公差 第1部分：未注尺寸公差
        """)

    # 第3章 定义
    with st.expander("📗 第3章 定义", expanded=True):
        st.markdown("""
        **3.1 未注公差值**

        未注公差值是指在图样上没有单独标注形位公差要求时，所应遵守的默认公差值。

        **3.2 未注公差等级**

        本标准规定了三个未注公差等级：

        - **H级（精密级）**：用于精度要求较高的场合

        - **K级（中等级）**：用于一般精度要求的场合

        - **L级（粗糙级）**：用于精度要求较低的场合

        **3.3 形位公差项目**

        **形状公差**：被测实际要素对其理想要素的允许变动量。

        | 项目 | 符号 | 是否需要基准 |
        |-----|------|------------|
        | 直线度 | — | 否 |
        | 平面度 | ▱ | 否 |
        | 圆度 | ○ | 否 |
        | 圆柱度 | ⌭ | 否 |

        **位置公差**：关联实际要素对基准所允许的变动全量。

        | 项目 | 符号 | 是否需要基准 |
        |-----|------|------------|
        | 平行度 | ∥ | 是 |
        | 垂直度 | ⊥ | 是 |
        | 倾斜度 | ∠ | 是 |
        | 同轴度 | ◎ | 是 |
        | 对称度 | ⌢ | 是 |
        | 位置度 | ⌖ | 是 |
        | 圆跳动 | ↗ | 是 |
        | 全跳动 | ⇗ | 是 |
        """)

    # 第4章 总则
    with st.expander("📗 第4章 总则", expanded=False):
        st.markdown("""
        **4.1 未注公差的标注**

        当零件图样上未标注形位公差时，应按本标准规定的未注公差值执行。

        **4.2 未注公差的标注位置**

        未注公差等级应在图样标题栏附近或技术要求中注明。

        示例：

        - "未注形位公差按GB/T 1184-H"

        - "未注形位公差按GB/T 1184-K"

        - "未注形位公差按GB/T 1184-L"

        **4.3 适用原则**

        - 一般情况下，采用K级（中等）未注公差

        - 精度要求较高时，采用H级（精密）未注公差

        - 精度要求较低时，采用L级（粗糙）未注公差
        """)

    # 第5章 形状和位置公差的未注公差值
    with st.expander("📗 第5章 形状和位置公差的未注公差值", expanded=True):
        st.markdown("""
        **5.1 直线度和平面度的未注公差值**

        | 公差等级 | 公差值（mm） |
        |---------|-------------|
        | H | 0.02~0.05 |
        | K | 0.05~0.1 |
        | L | 0.1~0.3 |

        选择公差值时，直线度应按其相应线的长度选择；平面度应按其表面的较长一侧或圆表面的直径选择。

        **5.2 圆度的未注公差值**

        圆度的未注公差值等于该要素的直径公差值，但不能大于5.3规定的跳动公差值。

        **5.3 圆柱度的未注公差值**

        圆柱度的未注公差值采用图样上注出的该要素的直径公差值。

        **5.4 平行度的未注公差值**

        平行度的未注公差值等于给出的尺寸公差值，或是直线度和平面度未注公差值中的相应公差值取较大者。

        **5.5 垂直度的未注公差值**

        垂直度的未注公差值见下表：

        | 被测要素长度mm | H级公差值 | K级公差值 | L级公差值 |
        |--------------|---------|---------|---------|
        | ≤100 | 0.2 | 0.4 | 0.6 |
        | 100~300 | 0.3 | 0.6 | 1.0 |
        | 300~1000 | 0.4 | 0.8 | 1.5 |
        | 1000~3000 | 0.5 | 1.0 | 2.0 |

        **5.6 对称度的未注公差值**

        | 被测要素长度mm | H级公差值 | K级公差值 | L级公差值 |
        |--------------|---------|---------|---------|
        | ≤100 | 0.2 | 0.4 | 0.6 |
        | 100~300 | 0.3 | 0.6 | 1.0 |
        | 300~1000 | 0.5 | 1.0 | 2.0 |
        | 1000~3000 | 0.7 | 1.5 | 3.0 |

        **5.7 圆跳动和全跳动的未注公差值**

        圆跳动和全跳动的未注公差值等于该要素的直径公差值。

        **5.8 线轮廓度和面轮廓度的未注公差值**

        线轮廓度和面轮廓度的未注公差值采用相对于被测要素轮廓的RADIUS公差带。
        """)

    # 第6章 图样上的表示法
    with st.expander("📗 第6章 图样上的表示法", expanded=False):
        st.markdown("""
        **6.1 未注公差等级的标注**

        未注公差等级应在技术要求或标题栏附近标注。

        标注示例：

        ```
        技术要求
        未注形位公差按GB/T 1184-H
        ```

        或

        ```
        未注形位公差：GB/T 1184-K
        ```

        **6.2 与其他标准的关系**

        如果同时采用ISO 2768-1（未注尺寸公差），应在图样上同时注明：

        ```
        一般公差：ISO 2768-m
        未注形位公差：GB/T 1184-K
        ```

        **6.3 图样解释**

        当图样上同时注出和未注形位公差时：

        - 注出的形位公差应符合其标注值

        - 未注的形位公差应符合本标准规定

        - 两者的要求应相互协调，不矛盾
        """)

    # 第7章 特殊情况
    with st.expander("📗 第7章 特殊情况", expanded=False):
        st.markdown("""
        **7.1 更严格的要求**

        当功能要求需要比未注公差更严格的形位公差时，应在图样上单独注出。

        **7.2 允许更大的公差**

        当制造精度比未注公差等级更低且不影响零件功能时，可采用更宽松的要求，但应在技术要求中说明。

        **7.3 检验原则**

        未注公差值的检验应采用与加工相同的检测原则：

        - 直线度：用刀口尺或平尺检验

        - 平面度：用平板或三坐标测量

        - 圆度：用圆度仪或投影仪检验

        - 垂直度：用直角尺或三坐标测量

        **7.4 争议处理**

        当供需双方对未注公差值产生争议时，应以零件的功能要求为准进行判定。
        """)

    # 附录A
    with st.expander("📗 附录A 未注公差值的解释", expanded=False):
        st.markdown("""
        **A.1 未注公差值的测量**

        未注公差值的测量应采用合理的检测方法。

        **A.2 检测方向**

        - 直线度：在任意方向测量

        - 平面度：在任意方向测量

        - 垂直度：在被测要素的法向方向测量

        **A.3 公差带位置**

        未注形位公差的公差带位置是浮动的，由实际要素的实际形状或位置确定。

        **A.4 符合性的判定**

        当实际要素的实际形状或位置被一个理想形状或位置所包容，且理想形状或位置与实际要素的接触点呈均匀分布时，认为符合未注公差要求。
        """)

    # 附录B
    with st.expander("📗 附录B 形位公差注出公差值", expanded=False):
        st.markdown("""
        **B.1 注出公差值的选择**

        当需要在图样上注出形位公差时，应按GB/T 1184-1996规定的公差值选择。

        **B.2 公差等级的应用**

        | 公差等级 | 应用举例 |
        |---------|---------|
        | 1~2级 | 精密量具、仪表、精密机床主轴 |
        | 3~4级 | 精密机床、通用机械的重要配合 |
        | 5~7级 | 一般机械的常用配合 |
        | 8~9级 | 非配合尺寸、粗糙加工表面 |
        | 10~12级 | 自由尺寸、冲压件、铸件 |

        **B.3 注出公差与未注公差的关系**

        - 注出公差值应严于或等于未注公差值

        - 两者不应矛盾

        - 设计时应综合考虑功能要求和工艺经济性
        """)


# ============================================================
# 第11节（续）：新增国家标准原文阅读函数
# ============================================================

def render_gbt18002_content(search_query, search_results):
    """显示 GB/T 1800.2-2020 标准内容"""
    st.markdown("### 📖 GB/T 1800.2-2020 极限与配合 第2部分")

    st.info("""
    **标准名称**：产品几何技术规范(GPS) 极限与配合 第2部分：标准公差等级和孔、轴极限偏差表  
    **适用范围**：光滑圆柱表面及单一尺寸要素的公差带选择  
    **发布日期**：2020-12-14 | **实施日期**：2021-07-01
    """)

    matched_locations = set()
    if search_results:
        for r in search_results:
            matched_locations.add(r["location"])

    # 标准公差数值表
    expand_it = "标准公差数值表" in " ".join(matched_locations)
    with st.expander("📊 标准公差数值表 (IT01-IT18)", expanded=expand_it):
        size_labels = [f"{r[0]}-{r[1]}" for r in SIZE_RANGES]
        it_grades_list = ["IT01", "IT0", "IT1", "IT2", "IT3", "IT4", "IT5", "IT6", "IT7", "IT8", "IT9", "IT10", "IT11", "IT12", "IT13", "IT14", "IT15", "IT16", "IT17", "IT18"]

        df_data = {"尺寸分段(mm)": size_labels}
        for grade in it_grades_list:
            if grade in IT_VALUES:
                df_data[grade] = IT_VALUES[grade]

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # 孔的基本偏差
    expand_hole = "孔基本偏差" in " ".join(matched_locations)
    with st.expander("📐 孔的基本偏差 (A-ZC)", expanded=expand_hole):
        st.markdown("""
        **孔的基本偏差代号**：A, B, C, CD, D, E, EF, F, FG, G, H, J, JS, K, M, N, P, R, S, T, U, V, X, Y, Z, ZA, ZB, ZC

        **基准孔 H**：下偏差 EI = 0

        **常用孔公差带**：
        - IT5: G5, H5, Js5, K5, M5, N5, P5, R5, S5, T5
        - IT6: C6, D6, E6, F6, G6, H6, Js6, K6, M6, N6, P6, R6, S6, T6, U6
        - IT7: D7, E7, F7, G7, H7, Js7, K7, M7, N7, P7, R7, S7, T7, U7
        - IT8: C8, D8, E8, F8, G8, H8, Js8, K8, M8, N8
        """)

    # 轴的基本偏差
    expand_shaft = "轴基本偏差" in " ".join(matched_locations)
    with st.expander("📐 轴的基本偏差 (a-zc)", expanded=expand_shaft):
        st.markdown("""
        **轴的基本偏差代号**：a, b, c, cd, d, e, ef, f, fg, g, h, j, js, k, m, n, p, r, s, t, u, v, x, y, z, za, zb, zc

        **基准轴 h**：上偏差 es = 0

        **常用轴公差带**：
        - IT5: g5, h5, js5, k5, m5, n5, p5, r5, s5, t5
        - IT6: c6, d6, e6, f6, g6, h6, js6, k6, m6, n6, p6, r6, s6, t6, u6
        - IT7: d7, e7, f7, g7, h7, js7, k7, m7, n7, p7, r7, s7, t7, u7
        - IT8: c8, d8, e8, f8, g8, h8, js8, k8, m8, n8
        """)


def render_gbt18002_fulltext():
    """GB/T 1800.2-2020 原文阅读"""
    st.markdown("### 📖 GB/T 1800.2-2020 原文")
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 极限与配合 第2部分：标准公差等级和孔、轴极限偏差表  
    **发布日期**：2020-12-14 | **实施日期**：2021-07-01 | **代替**：GB/T 1800.2-2009  
    **ICS分类**：17.040.10 | **中国标准分类号**：J04
    """)

    with st.expander("📑 本标准章节目录", expanded=True):
        chapters = [
            ("第1章", "范围"),
            ("第2章", "规范性引用文件"),
            ("第3章", "术语和定义"),
            ("第4章", "标准公差等级"),
            ("第5章", "孔的基本偏差数值"),
            ("第6章", "轴的基本偏差数值"),
            ("第7章", "极限偏差表"),
        ]
        for ch, title in chapters:
            st.write(f"**{ch}** {title}")

    with st.expander("📗 第1章 范围", expanded=False):
        st.markdown("""
        GB/T 1800的本部分规定了孔和轴的标准公差等级和极限偏差数值。

        本部分适用于具有圆柱形表面的光滑工件，也适用于其他表面或结构的单一尺寸要素。
        """)

    with st.expander("📗 第4章 标准公差等级", expanded=True):
        st.markdown("""
        **4.1 标准公差等级代号**

        标准公差等级用 IT 表示，分为 IT01、IT0、IT1 至 IT18 共 20 个等级。

        **4.2 标准公差数值表**

        标准公差数值取决于公称尺寸所在的尺寸分段和公差等级。

        本部分提供了完整的 IT01 至 IT18 标准公差数值表。
        """)

    with st.expander("📗 第5章 孔的基本偏差数值", expanded=False):
        st.markdown("""
        **5.1 孔的基本偏差代号**

        孔的基本偏差用大写字母表示：A、B、C、CD、D、E、EF、F、FG、G、H、J、JS、K、M、N、P、R、S、T、U、V、X、Y、Z、ZA、ZB、ZC

        **5.2 基准孔**

        基准孔的基本偏差代号为 H，其下偏差 EI = 0。

        **5.3 基本偏差数值表**

        本部分提供了公称尺寸至 3150mm 的孔基本偏差数值表。
        """)

    with st.expander("📗 第6章 轴的基本偏差数值", expanded=False):
        st.markdown("""
        **6.1 轴的基本偏差代号**

        轴的基本偏差用小写字母表示：a、b、c、cd、d、e、ef、f、fg、g、h、j、js、k、m、n、p、r、s、t、u、v、x、y、z、za、zb、zc

        **6.2 基准轴**

        基准轴的基本偏差代号为 h，其上偏差 es = 0。

        **6.3 基本偏差数值表**

        本部分提供了公称尺寸至 3150mm 的轴基本偏差数值表。
        """)

    with st.expander("📗 第7章 极限偏差表", expanded=True):
        st.markdown("""
        **7.1 孔的极限偏差**

        本部分提供了常用孔公差带的极限偏差表，包括：
        - 公称尺寸至 500mm 的优先和常用孔公差带
        - 公称尺寸 500mm 至 3150mm 的孔公差带

        **7.2 轴的极限偏差**

        本部分提供了常用轴公差带的极限偏差表，包括：
        - 公称尺寸至 500mm 的优先和常用轴公差带
        - 公称尺寸 500mm 至 3150mm 的轴公差带
        """)


def render_gbt17851_content(search_query, search_results):
    """显示 GB/T 17851-2010 标准内容"""
    st.markdown("### 📖 GB/T 17851-2010 产品几何技术规范(GPS) 基准和基准体系")

    st.info("""
    **标准名称**：产品几何技术规范(GPS) 几何公差 基准和基准体系  
    **适用范围**：机械零件几何公差标注中基准和基准体系的建立与应用  
    **发布日期**：2011-01-10 | **实施日期**：2011-10-01
    """)

    matched_locations = set()
    if search_results:
        for r in search_results:
            matched_locations.add(r["location"])

    expand_datum = "基准" in " ".join(matched_locations)
    with st.expander("📐 基准和基准体系", expanded=expand_datum):
        st.markdown("""
        **基准**：用来定义公差带位置或方向的理想要素。

        **基准要素**：零件上用来建立基准的实际要素。

        **基准体系**：由两个或三个单独的基准构成的组合，用于确定被测要素的方向或位置。

        **三基面体系**：由三个相互垂直的平面组成的基准体系。
        """)

    expand_symbol = "基准符号" in " ".join(matched_locations)
    with st.expander("🔣 基准符号", expanded=expand_symbol):
        st.markdown("""
        **基准符号组成**：
        - 大写字母（A、B、C...）
        - 细实线连线
        - 涂黑或空白的三角形

        **基准字母标注**：
        - 第一基准：A
        - 第二基准：B
        - 第三基准：C
        """)


def render_gbt17851_fulltext():
    """GB/T 17851-2010 原文阅读"""
    st.markdown("### 📖 GB/T 17851-2010 原文")
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 几何公差 基准和基准体系  
    **发布日期**：2011-01-10 | **实施日期**：2011-10-01 | **代替**：GB/T 17851-1999  
    **ICS分类**：17.040.10 | **中国标准分类号**：J04  
    **与ISO标准的对应关系**：ISO 5459:1981（NEQ，非等效）
    """)

    with st.expander("📑 本标准章节目录", expanded=True):
        chapters = [
            ("第1章", "范围"),
            ("第2章", "规范性引用文件"),
            ("第3章", "术语和定义"),
            ("第4章", "基准的建立"),
            ("第5章", "基准体系"),
            ("第6章", "基准目标"),
            ("第7章", "图样标注"),
        ]
        for ch, title in chapters:
            st.write(f"**{ch}** {title}")

    with st.expander("📗 第3章 术语和定义", expanded=True):
        st.markdown("""
        **3.1 基准 (Datum)**

        用来定义公差带位置或方向的理想要素。基准是理论上的精确几何要素，如理想平面、理想轴线等。

        **3.2 基准要素 (Datum Feature)**

        零件上用来建立基准的实际要素。基准要素是实际存在的零件表面或特征。

        **3.3 模拟基准要素 (Simulated Datum Feature)**

        在检测过程中用来代替基准要素的精确几何要素。如检测平板、心轴、V形块等。

        **3.4 基准体系 (Datum System)**

        由两个或三个单独的基准构成的组合，用于确定被测要素的方向或位置。

        **3.5 三基面体系 (Three-plane Datum System)**

        由三个相互垂直的平面组成的基准体系。这是最常见的基准体系形式。

        **3.6 基准目标 (Datum Target)**

        在基准要素上指定的点、线或局部区域，用于建立基准。
        """)

    with st.expander("📗 第4章 基准的建立", expanded=False):
        st.markdown("""
        **4.1 单一基准的建立**

        当基准要素是单一表面时，基准是该表面的理想平面。

        当基准要素是单一圆柱面时，基准是该圆柱面的理想轴线。

        **4.2 公共基准的建立**

        公共基准由两个同类要素共同建立，如两个平行平面建立公共基准平面。

        **4.3 基准与模拟基准要素的关系**

        基准是理想要素，模拟基准要素是实际检测中使用的精确几何要素。

        模拟基准要素应与基准要素稳定接触，接触状态应符合最小条件。
        """)

    with st.expander("📗 第5章 基准体系", expanded=True):
        st.markdown("""
        **5.1 三基面体系的建立**

        三基面体系由三个相互垂直的基准平面组成：
        - 第一基准平面（A）：通常选择最主要的定位面
        - 第二基准平面（B）：垂直于第一基准平面
        - 第三基准平面（C）：垂直于第一和第二基准平面

        **5.2 基准的顺序**

        基准的顺序很重要，第一基准限制的自由度最多，第三基准限制的自由度最少。

        **5.3 基准体系的标注**

        在公差框格的第三格及以后标注基准字母，顺序表示基准的优先顺序。

        示例：| 平行度 | 0.05 | A | B | C |
        """)

    with st.expander("📗 第6章 基准目标", expanded=False):
        st.markdown("""
        **6.1 基准目标的使用场合**

        当基准要素为不规则表面、铸造表面或锻造表面时，使用基准目标建立基准。

        **6.2 基准目标的类型**

        - 点目标：用符号 × 表示
        - 线目标：用双点划线表示
        - 面目标：用虚线表示的局部区域

        **6.3 基准目标的标注**

        基准目标用细实线圆表示，内部标注基准字母和目标编号。
        """)

    with st.expander("📗 第7章 图样标注", expanded=False):
        st.markdown("""
        **7.1 基准符号的标注**

        基准符号由以下部分组成：
        - 大写字母（A、B、C...，I、O、Q除外）
        - 细实线连线
        - 涂黑或空白的等边三角形

        **7.2 基准字母的选用**

        - 第一基准：A
        - 第二基准：B
        - 第三基准：C
        - 依此类推...

        **7.3 基准要素的标注位置**

        基准符号应标注在：
        - 基准要素的轮廓线或其延长线上
        - 基准要素的尺寸引出线
        - 公差框格的第三格及以后
        """)


def render_gbt4249_content(search_query, search_results):
    """显示 GB/T 4249-2009 标准内容"""
    st.markdown("### 📖 GB/T 4249-2009 产品几何技术规范(GPS) 公差原则")

    st.info("""
    **标准名称**：产品几何技术规范(GPS) 公差原则  
    **适用范围**：机械零件尺寸公差与几何公差的关系及公差原则的应用  
    **发布日期**：2009-03-16 | **实施日期**：2009-11-01
    """)

    matched_locations = set()
    if search_results:
        for r in search_results:
            matched_locations.add(r["location"])

    expand_principle = "公差原则" in " ".join(matched_locations)
    with st.expander("📐 公差原则", expanded=expand_principle):
        st.markdown("""
        **独立原则**：尺寸公差与几何公差分别独立，互不影响。

        **相关要求**：尺寸公差与几何公差相互关联，包括：
        - 包容要求（E）
        - 最大实体要求（M）
        - 最小实体要求（L）
        - 可逆要求（R）
        """)

    expand_e = "包容要求" in " ".join(matched_locations)
    with st.expander("🔘 包容要求 (E)", expanded=expand_e):
        st.markdown("""
        **包容要求**适用于单一要素，要求实际要素处处不得超越最大实体边界。

        标注方法：在尺寸公差后加注符号 Ⓔ

        应用场合：需要保证配合性质的场合，如轴承配合面。
        """)

    expand_m = "最大实体要求" in " ".join(matched_locations)
    with st.expander("🔘 最大实体要求 (M)", expanded=expand_m):
        st.markdown("""
        **最大实体要求**适用于中心要素，当实际要素偏离最大实体状态时，允许几何公差获得补偿。

        标注方法：在几何公差值后加注符号 Ⓜ

        应用场合：需要保证装配互换性的场合，如螺栓孔组。
        """)


def render_gbt4249_fulltext():
    """GB/T 4249-2009 原文阅读"""
    st.markdown("### 📖 GB/T 4249-2009 原文")
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 公差原则  
    **发布日期**：2009-03-16 | **实施日期**：2009-11-01 | **代替**：GB/T 4249-1996  
    **ICS分类**：17.040.10 | **中国标准分类号**：J04  
    **与ISO标准的对应关系**：ISO 8015:1985（NEQ，非等效）
    """)

    with st.expander("📑 本标准章节目录", expanded=True):
        chapters = [
            ("第1章", "范围"),
            ("第2章", "规范性引用文件"),
            ("第3章", "术语和定义"),
            ("第4章", "独立原则"),
            ("第5章", "相关要求"),
            ("第6章", "包容要求"),
            ("第7章", "最大实体要求"),
            ("第8章", "最小实体要求"),
            ("第9章", "可逆要求"),
        ]
        for ch, title in chapters:
            st.write(f"**{ch}** {title}")

    with st.expander("📗 第3章 术语和定义", expanded=True):
        st.markdown("""
        **3.1 公差原则 (Tolerance Principle)**

        确定尺寸公差与几何公差之间相互关系的原则。

        **3.2 独立原则 (Independency Principle)**

        图样上给定的每一个尺寸公差和几何公差均是独立的，应分别满足要求。

        **3.3 相关要求 (Related Requirement)**

        尺寸公差与几何公差相互有关的公差要求。

        **3.4 最大实体状态 (Maximum Material Condition, MMC)**

        实际要素在给定长度上处处位于尺寸极限之内，并具有实体最大时的状态。

        **3.5 最小实体状态 (Least Material Condition, LMC)**

        实际要素在给定长度上处处位于尺寸极限之内，并具有实体最小时的状态。

        **3.6 最大实体实效状态 (Maximum Material Virtual Condition, MMVC)**

        实际要素处于最大实体状态，且其中心要素的几何误差等于图样上标注的几何公差值时的状态。

        **3.7 边界 (Boundary)**

        由设计给定的具有理想形状的极限包容面。
        """)

    with st.expander("📗 第4章 独立原则", expanded=False):
        st.markdown("""
        **4.1 独立原则的定义**

        图样上给定的每一个尺寸公差和几何公差均是独立的，应分别满足要求。

        **4.2 独立原则的应用**

        独立原则是尺寸公差和几何公差关系的基本原则，除非另有规定，独立原则适用于一切要素。

        **4.3 独立原则的标注**

        独立原则不需要特别标注，是默认的公差原则。

        如需明确采用独立原则，可在图样或技术文件中注明："公差原则按GB/T 4249"。
        """)

    with st.expander("📗 第5章 相关要求", expanded=True):
        st.markdown("""
        **5.1 相关要求的定义**

        尺寸公差与几何公差相互有关的公差要求。

        **5.2 相关要求的类型**

        - **包容要求（E）**：适用于单一要素
        - **最大实体要求（M）**：适用于中心要素
        - **最小实体要求（L）**：适用于中心要素
        - **可逆要求（R）**：可附加于最大实体要求或最小实体要求

        **5.3 相关要求的标注**

        相关要求用特定符号标注在图样上：
        - 包容要求：Ⓔ
        - 最大实体要求：Ⓜ
        - 最小实体要求：Ⓛ
        - 可逆要求：Ⓡ
        """)

    with st.expander("📗 第6章 包容要求", expanded=False):
        st.markdown("""
        **6.1 包容要求的定义**

        包容要求适用于单一要素，要求实际要素处处不得超越最大实体边界。

        **6.2 包容要求的标注**

        在尺寸公差后加注包容要求符号 Ⓔ。

        示例：ø50H7 Ⓔ 或 ø50+0.025/0 Ⓔ

        **6.3 包容要求的应用**

        包容要求主要用于需要保证配合性质的场合，如：
        - 轴承配合面
        - 精密配合孔、轴
        - 需要保证最小间隙或最大过盈的场合
        """)

    with st.expander("📗 第7章 最大实体要求", expanded=True):
        st.markdown("""
        **7.1 最大实体要求的定义**

        最大实体要求适用于中心要素，当实际要素偏离最大实体状态时，允许几何公差获得补偿。

        **7.2 最大实体要求的标注**

        在几何公差值后加注最大实体要求符号 Ⓜ。

        示例：| 位置度 | φ0.5 Ⓜ | A | B | C |

        **7.3 最大实体要求的应用**

        最大实体要求主要用于需要保证装配互换性的场合，如：
        - 螺栓孔组
        - 销孔组
        - 需要保证装配但不需要精密配合的场合

        **7.4 最大实体要求的优点**

        - 放宽了几何公差要求，降低了加工成本
        - 仍能保证装配互换性
        - 适用于大批量生产
        """)

    with st.expander("📗 第8章 最小实体要求", expanded=False):
        st.markdown("""
        **8.1 最小实体要求的定义**

        最小实体要求适用于中心要素，当实际要素偏离最小实体状态时，允许几何公差获得补偿。

        **8.2 最小实体要求的标注**

        在几何公差值后加注最小实体要求符号 Ⓛ。

        示例：| 位置度 | φ0.5 Ⓛ | A | B | C |

        **8.3 最小实体要求的应用**

        最小实体要求主要用于需要保证最小壁厚的场合，如：
        - 薄壁零件
        - 需要保证强度的孔、轴
        """)

    with st.expander("📗 第9章 可逆要求", expanded=False):
        st.markdown("""
        **9.1 可逆要求的定义**

        可逆要求是一种附加要求，当几何误差小于图样上标注的几何公差值时，允许尺寸公差获得补偿。

        **9.2 可逆要求的标注**

        在最大实体要求或最小实体要求后加注可逆要求符号 Ⓡ。

        示例：| 位置度 | φ0.5 Ⓜ Ⓡ | A | B | C |

        **9.3 可逆要求的应用**

        可逆要求提供了更大的公差补偿灵活性，适用于：
        - 需要最大公差补偿的场合
        - 精密配合与装配互换性并重的场合
        """)


def render_gbt45683_content(search_query, search_results):
    """显示 GB/T 45683-2025 标准内容"""
    st.markdown("### 📖 GB/T 45683-2025 产品几何技术规范(GPS) 一般几何规范")

    st.info("""
    **标准名称**：产品几何技术规范(GPS) 一般几何规范  
    **适用范围**：机械产品几何规范的通用要求和操作集  
    **发布日期**：2025-XX-XX | **实施日期**：2025-XX-XX
    """)

    matched_locations = set()
    if search_results:
        for r in search_results:
            matched_locations.add(r["location"])

    expand_gps = "GPS体系" in " ".join(matched_locations)
    with st.expander("🌐 GPS体系概述", expanded=expand_gps):
        st.markdown("""
        **GPS (Geometrical Product Specification)**：产品几何技术规范

        GPS体系包括：
        - 尺寸公差
        - 几何公差（形状、方向、位置、跳动）
        - 表面结构（粗糙度、波纹度）
        - 螺纹、齿轮、键等特殊要素公差
        """)

    expand_operation = "规范操作集" in " ".join(matched_locations)
    with st.expander("⚙️ 规范操作集", expanded=expand_operation):
        st.markdown("""
        **规范操作集**是GPS标准的核心概念，用于定义几何特征的规范要求。

        包括：
        - 分离操作
        - 提取操作
        - 滤波操作
        - 拟合操作
        - 集合操作
        """)


def render_gbt45683_fulltext():
    """GB/T 45683-2025 原文阅读"""
    st.markdown("### 📖 GB/T 45683-2025 原文")
    st.info("""
    **标准名称**：产品几何技术规范(GPS) 一般几何规范  
    **发布日期**：2025年 | **实施日期**：2025年  
    **ICS分类**：17.040.10 | **中国标准分类号**：J04  
    **与ISO标准的对应关系**：基于ISO GPS体系最新发展
    """)

    with st.expander("📑 本标准章节目录", expanded=True):
        chapters = [
            ("第1章", "范围"),
            ("第2章", "规范性引用文件"),
            ("第3章", "术语和定义"),
            ("第4章", "GPS体系概述"),
            ("第5章", "规范操作集"),
            ("第6章", "缺省规范"),
            ("第7章", "图样标注规则"),
        ]
        for ch, title in chapters:
            st.write(f"**{ch}** {title}")

    with st.expander("📗 第1章 范围", expanded=False):
        st.markdown("""
        本标准规定了产品几何技术规范（GPS）的一般几何规范，包括：

        - GPS体系的总体框架
        - 规范操作集的定义和应用
        - 缺省规范的规则
        - 图样标注的基本要求

        本标准适用于机械产品的几何规范设计与标注。
        """)

    with st.expander("📗 第3章 术语和定义", expanded=True):
        st.markdown("""
        **3.1 GPS (Geometrical Product Specification)**

        产品几何技术规范，是用于描述产品几何特性的完整标准体系。

        **3.2 规范操作集 (Specification Operator)**

        用于定义几何特征规范要求的一系列有序操作的集合。

        **3.3 缺省规范 (Default Specification)**

        当图样上没有明确标注时，自动适用的规范要求。

        **3.4 特征 (Feature)**

        工件上的特定几何要素，如平面、圆柱面、球面等。

        **3.5 表面模型 (Surface Model)**

        用于描述工件几何特性的理想化数学模型。
        """)

    with st.expander("📗 第4章 GPS体系概述", expanded=True):
        st.markdown("""
        **4.1 GPS体系的组成**

        GPS体系包括以下主要部分：

        - **基础标准**：术语、定义、通则
        - **全局标准**：尺寸公差、几何公差、表面结构
        - **一般标准**：一般几何规范、基准体系、公差原则
        - **综合标准**：螺纹、齿轮、花键等特殊要素
        - **测量标准**：测量方法、测量不确定度

        **4.2 GPS体系的特点**

        - 以数学定义为基础
        - 采用操作集方法
        - 支持数字化设计和检测
        - 与ISO标准体系协调一致

        **4.3 GPS标准的应用**

        GPS标准应用于产品生命周期的各个阶段：
        - 设计阶段：几何规范定义
        - 制造阶段：工艺规划
        - 检测阶段：合格评定
        """)

    with st.expander("📗 第5章 规范操作集", expanded=False):
        st.markdown("""
        **5.1 规范操作集的概念**

        规范操作集是GPS标准的核心，用于将几何特征的实际状态与规范要求进行比较。

        **5.2 规范操作集的类型**

        - **分离操作**：从整体中提取特定特征
        - **提取操作**：从特征中提取特定点集
        - **滤波操作**：分离不同频率的成分
        - **拟合操作**：用理想几何要素逼近实际要素
        - **集合操作**：对点集进行集合运算
        - **评估操作**：计算特征参数值

        **5.3 规范操作集的应用**

        每个GPS规范都对应一个特定的规范操作集，用于：
        - 明确规范要求
        - 指导检测方法
        - 保证规范的一致性
        """)

    with st.expander("📗 第6章 缺省规范", expanded=False):
        st.markdown("""
        **6.1 缺省规范的概念**

        当图样上没有明确标注时，自动适用的规范要求称为缺省规范。

        **6.2 缺省规范的内容**

        - 缺省尺寸公差
        - 缺省几何公差
        - 缺省表面粗糙度
        - 缺省基准体系

        **6.3 缺省规范的标注**

        缺省规范应在技术文件中明确说明，如：
        - "未注尺寸公差按GB/T 1804-m"
        - "未注几何公差按GB/T 1184-K"
        - "未注表面粗糙度Ra6.3"
        """)

    with st.expander("📗 第7章 图样标注规则", expanded=False):
        st.markdown("""
        **7.1 图样标注的基本要求**

        GPS图样标注应满足以下要求：
        - 清晰、完整、无歧义
        - 符合国家标准规定
        - 便于理解和执行

        **7.2 图样标注的要素**

        GPS图样标注包括：
        - 尺寸公差标注
        - 几何公差标注
        - 表面结构标注
        - 基准和基准体系标注
        - 特殊要求标注

        **7.3 数字化标注**

        支持数字化设计和制造的GPS标注：
        - 基于模型的定义（MBD）
        - 产品制造信息（PMI）
        - 与CAD/CAM/CAQ系统集成
        """)


