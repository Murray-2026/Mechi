"""智能推荐系统模块 - 基于工况的配合推荐、配合实时计算、基准制选择建议"""

def search_working_conditions(query, recommendations):
    """根据工况描述搜索推荐"""
    if not query:
        return []
    results = []
    query_lower = query.lower()
    for rec in recommendations:
        # 匹配工况名称
        if query in rec["condition"] or any(kw in query_lower for kw in rec["keywords"]):
            results.append(rec)
    return results


def calculate_fit_properties(hole_upper, hole_lower, shaft_upper, shaft_lower):
    """
    计算配合性质（间隙/过盈）
    返回: min_clearance, max_clearance, min_interference, max_interference, fit_type
    """
    min_clearance = hole_lower - shaft_upper  # 最小间隙
    max_clearance = hole_upper - shaft_lower  # 最大间隙
    min_interference = shaft_lower - hole_upper  # 最小过盈
    max_interference = shaft_upper - hole_lower  # 最大过盈

    if min_clearance >= 0:
        fit_type = "间隙配合"
        fit_color = "#27ae60"
        fit_icon = "↔"
    elif max_interference <= 0:
        fit_type = "过渡配合"
        fit_color = "#f39c12"
        fit_icon = "⇄"
    else:
        fit_type = "过盈配合"
        fit_color = "#e74c3c"
        fit_icon = "⇒"

    return {
        "min_clearance": round(min_clearance, 4),
        "max_clearance": round(max_clearance, 4),
        "min_interference": round(min_interference, 4),
        "max_interference": round(max_interference, 4),
        "fit_type": fit_type,
        "fit_color": fit_color,
        "fit_icon": fit_icon,
    }


def render_smart_recommend_tab():
    """渲染智能推荐系统标签页"""
    import streamlit as st
    from data.cost_process_data import WORKING_CONDITION_RECOMMENDATIONS
    from data.tolerance_data import SIZE_RANGES, IT_VALUES
    from data.fit_data import COMMON_FITS_INFO
    from modules.utils import query_tolerance

    st.markdown("## 🤖 智能配合推荐系统")

    # Tab切换
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(["🎯 工况推荐", "📊 配合计算", "🔧 基准制选择", "📦 结构案例库"])

    with sub_tab1:
        st.markdown("### 基于工况条件的智能推荐")
        st.markdown("输入您的工况条件（如\"旋转精度要求高\"、\"承受较大载荷\"等），系统自动推荐合适的配合。")

        condition = st.text_input("工况条件描述", placeholder="例如：旋转精度要求高、承受较大载荷、需要经常拆卸、滑动运动...")

        if st.button("🔍 获取推荐", type="primary", use_container_width=True):
            if not condition:
                st.warning("请输入工况条件")
                return

            results = search_working_conditions(condition, WORKING_CONDITION_RECOMMENDATIONS)

            if not results:
                st.warning("未找到匹配的工况推荐。请尝试其他关键词，如：旋转、载荷、拆卸、滑动、高速、密封、定位、高温")
                return

            for rec in results:
                # 工况卡片
                card_html = (
                    '<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);'
                    'padding:14px;border-radius:8px;margin-bottom:12px;">'
                    '<div style="color:white;font-size:18px;font-weight:bold;">' + rec["condition"] + '</div></div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                for fit in rec["recommended_fits"]:
                    fit_html = (
                        '<div style="background:white;border:1px solid #e0e0e0;border-radius:8px;'
                        'padding:14px;margin-bottom:8px;">'
                        '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
                        '<span style="font-size:20px;font-weight:bold;color:#2c3e50;">' + fit["fit"] + '</span>'
                        '<span style="font-size:12px;background:#e8f0fe;color:#1a73e8;padding:2px 8px;'
                        'border-radius:10px;">' + fit["type"] + '</span></div>'
                        '<div style="font-size:13px;color:#333;line-height:1.5;">' + fit["reason"] + '</div>'
                        '<div style="font-size:12px;color:#7f8c8d;margin-top:4px;">装配方式：' + fit["assembly"] + '</div></div>'
                    )
                    st.markdown(fit_html, unsafe_allow_html=True)

                # 附加建议
                if rec.get("geo_tolerance"):
                    st.markdown("**📐 推荐形位公差**：" + rec["geo_tolerance"])
                if rec.get("roughness"):
                    st.markdown("**🔲 推荐表面粗糙度**：" + rec["roughness"])
                if rec.get("note"):
                    st.info(rec["note"])
                st.markdown("---")

    with sub_tab2:
        st.markdown("### 配合性质实时计算")
        st.markdown("选择配合代号和公称尺寸，自动计算最小/最大间隙或过盈量。")

        col1, col2 = st.columns(2)
        with col1:
            nominal = st.number_input("公称尺寸 (mm)", value=50.0, min_value=0.1)
        with col2:
            fit_code = st.text_input("配合代号", value="H7/f6", placeholder="如 H7/f6、H7/k6、H7/p6")

        if st.button("计算配合性质", type="primary", use_container_width=True):
            try:
                # 解析配合代号
                hole_code = fit_code.split("/")[0].strip()
                shaft_code = fit_code.split("/")[1].strip()

                hole_tol = query_tolerance(hole_code, nominal)
                shaft_tol = query_tolerance(shaft_code, nominal)

                if hole_tol is None or shaft_tol is None:
                    st.error("无法查询该配合代号，请检查输入")
                    return

                result = calculate_fit_properties(
                    hole_tol["ES"], hole_tol["EI"],
                    shaft_tol["ES"], shaft_tol["EI"]
                )

                # 结果展示
                result_html = (
                    '<div style="background:' + result["fit_color"] + '15;border:2px solid ' + result["fit_color"] + ';'
                    'border-radius:12px;padding:20px;text-align:center;margin-bottom:16px;">'
                    '<div style="font-size:14px;color:#666;margin-bottom:4px;">配合类型</div>'
                    '<div style="font-size:28px;font-weight:bold;color:' + result["fit_color"] + ';">'
                    + result["fit_icon"] + ' ' + result["fit_type"] + '</div>'
                    '<div style="font-size:16px;color:#333;margin-top:4px;">' + fit_code + ' (ø' + str(nominal) + ')</div></div>'
                )
                st.markdown(result_html, unsafe_allow_html=True)

                # 详细数据
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("孔公差", "ES=" + str(hole_tol["ES"]) + ", EI=" + str(hole_tol["EI"]))
                with col_b:
                    st.metric("轴公差", "es=" + str(shaft_tol["es"]) + ", ei=" + str(shaft_tol["ei"]))

                col_c, col_d = st.columns(2)
                with col_c:
                    st.metric("最大间隙", str(result["max_clearance"]) + " mm")
                with col_d:
                    st.metric("最小间隙", str(result["min_clearance"]) + " mm")

                col_e, col_f = st.columns(2)
                with col_e:
                    st.metric("最大过盈", str(result["max_interference"]) + " mm")
                with col_f:
                    st.metric("最小过盈", str(result["min_interference"]) + " mm")

            except Exception as e:
                st.error("计算出错：" + str(e))

    with sub_tab3:
        st.markdown("### 基准制选择建议")

        st.markdown("""
        **基孔制 vs 基轴制选择原则：**

        | 对比项 | 基孔制 | 基轴制 |
        |-------|--------|--------|
        | 基准件 | 孔（H） | 轴（h） |
        | 基准偏差 | EI=0 | es=0 |
        | 优先程度 | ✅ 优先选用 | 特殊场合使用 |
        | 刀具需求 | 减少孔加工刀具规格 | 减少轴加工刀具规格 |
        | 成本 | 较低（孔加工刀具贵） | 较高 |

        **推荐采用基孔制的场合：**
        1. 一般机械设计（默认选择）
        2. 孔加工需要定值刀具（钻头、铰刀、拉刀）
        3. 同一公称尺寸的轴只需一种基本偏差

        **推荐采用基轴制的场合：**
        1. 同一轴与多个不同配合要求的孔配合（如活塞销）
        2. 采用冷拉圆钢作轴，不再加工外圆
        3. 标准件外径配合（如滚动轴承外圈与座孔）
        4. 纺织机械中的光轴配合
        """)

        # 交互式决策
        st.markdown("---")
        st.markdown("### 🔍 基准制决策助手")

        q1 = st.radio("同一轴上是否有多个不同配合要求的孔？", ["否", "是"], index=0)
        q2 = st.radio("是否使用冷拉圆钢（不加工外圆）？", ["否", "是"], index=0)
        q3 = st.radio("是否为标准件外径配合（如轴承外圈）？", ["否", "是"], index=0)

        if q1 == "是" or q2 == "是" or q3 == "是":
            recommendation = "基轴制"
            reason = ""
            if q1 == "是": reason += "• 同一轴多孔配合 → 基轴制可减少轴的规格\n"
            if q2 == "是": reason += "• 冷拉圆钢不加工 → 基轴制利用标准轴径\n"
            if q3 == "是": reason += "• 标准件外径 → 基轴制与标准件配合\n"

            st.markdown(
                '<div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:16px;">'
                '<div style="font-size:18px;font-weight:bold;color:#856404;">推荐：' + recommendation + '</div>'
                '<div style="font-size:13px;color:#856404;margin-top:8px;white-space:pre-line;">' + reason + '</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background:#d4edda;border:1px solid #28a745;border-radius:8px;padding:16px;">'
                '<div style="font-size:18px;font-weight:bold;color:#155724;">推荐：基孔制（优先）</div>'
                '<div style="font-size:13px;color:#155724;margin-top:8px;">'
                '• 一般机械设计默认选择基孔制\n'
                '• 减少孔加工刀具规格，降低制造成本\n'
                '• 加工工艺成熟，应用广泛</div></div>',
                unsafe_allow_html=True
            )

    # ==================== 结构案例库 ====================
    with sub_tab4:
        from data.case_data import MECHANICAL_CASES

        st.markdown("### 📦 常见机械结构公差案例库")
        st.markdown("涵盖轴承安装、键连接、密封结构、销连接、齿轮传动等经典设计案例，提供设计要点与常见公差取值。")

        # 分类选择
        category_names = [cat["icon"] + " " + cat["category"] for cat in MECHANICAL_CASES]
        selected_cat = st.selectbox("选择结构类别", category_names, index=0)

        cat_data = next(cat for cat in MECHANICAL_CASES if cat["icon"] + " " + cat["category"] == selected_cat)

        for case in cat_data["cases"]:
            # 案例标题卡片
            case_title_html = (
                '<div style="background:linear-gradient(135deg,#2193b0 0%,#6dd5ed 100%);'
                'padding:14px;border-radius:10px;margin-bottom:12px;margin-top:20px;">'
                '<div style="color:white;font-size:18px;font-weight:bold;">' + case["name"] + '</div>'
                '<div style="color:rgba(255,255,255,0.85);font-size:13px;margin-top:4px;">' + case["description"] + '</div></div>'
            )
            st.markdown(case_title_html, unsafe_allow_html=True)

            # SVG结构示意图
            if case.get("svg_diagram"):
                svg_container = (
                    '<div style="background:white;border:1px solid #e0e0e0;border-radius:10px;'
                    'padding:16px;margin-bottom:16px;text-align:center;">'
                    '<div style="font-size:14px;font-weight:bold;color:#374151;margin-bottom:12px;">📐 结构示意图</div>'
                    + case["svg_diagram"] +
                    '</div>'
                )
                st.markdown(svg_container, unsafe_allow_html=True)

            # 设计要点
            with st.expander("📝 设计要点", expanded=True):
                for i, point in enumerate(case["design_points"], 1):
                    st.markdown(f"**{i}.** {point}")

            # 公差取值表
            with st.expander("📊 推荐公差取值", expanded=True):
                import pandas as pd
                tol_df = pd.DataFrame(case["tolerance_values"])
                tol_df.columns = ["部位", "公差带/要求", "说明"]
                st.dataframe(tol_df, use_container_width=True, hide_index=True)

            # 常见错误
            with st.expander("⚠️ 常见错误", expanded=False):
                for mistake in case["common_mistakes"]:
                    st.markdown(
                        '<div style="background:#fff5f5;border-left:3px solid #e74c3c;padding:8px 12px;'
                        'margin-bottom:6px;border-radius:0 6px 6px 0;font-size:13px;color:#c0392b;">'
                        '❌ ' + mistake + '</div>',
                        unsafe_allow_html=True
                    )
