"""工程工具模块 - 成本关联、热膨胀计算、表面粗糙度、材料库、过盈压装力"""

def render_engineering_tools_tab():
    """渲染工程工具标签页"""
    import streamlit as st
    from data.cost_process_data import (
        TOLERANCE_COST_DATA, PROCESS_PRECISION,
        THERMAL_EXPANSION_DATA, SURFACE_ROUGHNESS_DATA
    )
    import pandas as pd

    sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs([
        "💰 公差等级-成本", "🌡️ 热膨胀计算", "🔲 表面粗糙度", "🛡️ 防错检查清单", "🔩 材料库"
    ])

    # ==================== 公差等级-成本关联 ====================
    with sub_tab1:
        st.markdown("### 💰 公差等级-成本关联")
        st.markdown("公差等级直接影响制造成本。了解成本关联有助于在精度与经济性之间做出平衡。")

        cost_df = pd.DataFrame([
            {"等级": k, "成本指数": v["cost_index"], "相对成本": v["relative_cost"],
             "相邻等级成本增幅": v["cost_increase"], "典型工艺": v["typical_process"]}
            for k, v in TOLERANCE_COST_DATA.items()
        ])
        st.dataframe(cost_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        selected_grade = st.selectbox("选择公差等级查看成本提示", list(TOLERANCE_COST_DATA.keys()), index=2)
        cost_info = TOLERANCE_COST_DATA[selected_grade]

        cost_html = (
            '<div style="background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);'
            'padding:16px;border-radius:8px;color:white;">'
            '<div style="font-size:20px;font-weight:bold;margin-bottom:8px;">' + selected_grade + ' 成本分析</div>'
            '<div style="font-size:14px;">成本指数：<b>' + str(cost_info["cost_index"]) + '</b>（以IT5为基准100）</div>'
            '<div style="font-size:14px;margin-top:4px;">' + cost_info["relative_cost"] + '</div>'
            '<div style="font-size:14px;margin-top:4px;">' + cost_info["cost_increase"] + '</div>'
            '<div style="font-size:14px;margin-top:4px;">推荐工艺：' + cost_info["typical_process"] + '</div></div>'
        )
        st.markdown(cost_html, unsafe_allow_html=True)

        with st.expander("🔧 常用加工工艺经济精度范围", expanded=True):
            process_df = pd.DataFrame(PROCESS_PRECISION)
            st.dataframe(process_df, use_container_width=True, hide_index=True)

    # ==================== 热膨胀计算 ====================
    with sub_tab2:
        st.markdown("### 🌡️ 热膨胀系数查询与计算")
        st.markdown("计算温度变化导致的尺寸变化：**ΔL = α × L × ΔT**")

        from data.case_data import MATERIAL_PROPERTIES

        # 获取内置材料库的膨胀系数
        mat_options = {m["material"]: m["alpha"] for m in MATERIAL_PROPERTIES}
        mat_names = list(mat_options.keys())

        # 也加回旧的材料选项
        old_materials = {m["material"]: m["coefficient"] for m in THERMAL_EXPANSION_DATA}

        selected_mat = st.selectbox("选择材料（内置材料库）", mat_names, index=5)
        alpha_val = mat_options[selected_mat]

        # 获取材料完整信息
        mat_info = next(m for m in MATERIAL_PROPERTIES if m["material"] == selected_mat)

        mat_card = (
            '<div style="background:#fff3e0;border:1px solid #ffb74d;border-radius:8px;padding:12px;margin-bottom:12px;">'
            '<div style="font-size:16px;font-weight:bold;color:#e65100;">' + mat_info["material"] + ' (' + mat_info["category"] + ')</div>'
            '<div style="font-size:14px;color:#333;">热膨胀系数 α = <b>' + str(mat_info["alpha"]) + ' × 10⁻⁶/°C</b></div>'
            '<div style="font-size:12px;color:#666;">密度: ' + str(mat_info["density"]) + ' g/cm³ | 弹性模量: ' + str(mat_info["elastic_modulus"]) + ' GPa</div>'
            '<div style="font-size:12px;color:#666;">屈服强度: ' + str(mat_info["yield_strength"]) + ' MPa | 抗拉强度: ' + str(mat_info["tensile_strength"]) + ' MPa</div>'
            '<div style="font-size:12px;color:#666;">备注: ' + mat_info["note"] + '</div></div>'
        )
        st.markdown(mat_card, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            L = st.number_input("原始长度 L (mm)", value=100.0, min_value=0.01)
        with col2:
            T1 = st.number_input("初始温度 (°C)", value=20.0)
        with col3:
            T2 = st.number_input("最终温度 (°C)", value=100.0)

        if st.button("计算热膨胀", type="primary", use_container_width=True):
            alpha = alpha_val * 1e-6
            delta_T = T2 - T1
            delta_L = alpha * L * delta_T
            L_new = L + delta_L

            result_html = (
                '<div style="background:#e3f2fd;border:1px solid #42a5f5;border-radius:8px;padding:16px;">'
                '<div style="font-size:14px;color:#1565c0;margin-bottom:8px;">计算公式：ΔL = α × L × ΔT</div>'
                '<div style="font-size:14px;color:#333;">ΔL = ' + str(alpha) + ' × ' + str(L) + ' × ' + str(delta_T) + '</div>'
                '<div style="font-size:20px;font-weight:bold;color:#0d47a1;margin-top:8px;">'
                'ΔL = ' + str(round(delta_L, 4)) + ' mm</div>'
                '<div style="font-size:14px;color:#333;margin-top:4px;">变化后长度：' + str(round(L_new, 4)) + ' mm</div>'
                '<div style="font-size:12px;color:#666;margin-top:8px;">'
                '💡 在精密配合设计中，应考虑热膨胀导致的尺寸变化，预留合理的配合间隙。</div></div>'
            )
            st.markdown(result_html, unsafe_allow_html=True)

    # ==================== 表面粗糙度推荐 ====================
    with sub_tab3:
        st.markdown("### 🔲 表面粗糙度关联推荐")
        st.markdown("表面粗糙度与加工工艺、成本密切相关。选择合适的粗糙度等级是平衡精度与成本的关键。")

        selected_ra = st.selectbox("选择粗糙度等级 Ra (μm)",
            [str(r["ra_value"]) for r in SURFACE_ROUGHNESS_DATA], index=4)
        ra_data = next(r for r in SURFACE_ROUGHNESS_DATA if str(r["ra_value"]) == selected_ra)

        ra_html = (
            '<div style="background:linear-gradient(135deg,#a8e063 0%,#56ab2f 100%);'
            'padding:16px;border-radius:8px;color:white;margin-bottom:12px;">'
            '<div style="font-size:20px;font-weight:bold;">Ra ' + selected_ra + ' μm (' + ra_data["grade"] + ')</div>'
            '<div style="font-size:14px;margin-top:8px;">推荐加工工艺：' + ra_data["process"] + '</div>'
            '<div style="font-size:14px;margin-top:4px;">典型应用：' + ra_data["application"] + '</div>'
            '<div style="font-size:14px;margin-top:4px;">' + ra_data["cost_note"] + '</div></div>'
        )
        st.markdown(ra_html, unsafe_allow_html=True)

        with st.expander("📊 表面粗糙度等级对照表", expanded=True):
            ra_df = pd.DataFrame(SURFACE_ROUGHNESS_DATA)
            st.dataframe(ra_df, use_container_width=True, hide_index=True)

    # ==================== 防错设计检查清单 ====================
    with sub_tab4:
        from data.case_data import POKAYOKE_CHECKLIST

        st.markdown("### 🛡️ 防错设计检查清单")
        st.markdown("帮助工程师在设计阶段排查常见错误，涵盖对称性、装配防错、公差标注、工艺可行性等方面。")

        category_names = [cat["icon"] + " " + cat["category"] for cat in POKAYOKE_CHECKLIST]
        selected_cat = st.selectbox("选择检查类别", category_names, index=0)

        cat_data = next(cat for cat in POKAYOKE_CHECKLIST if cat["icon"] + " " + cat["category"] == selected_cat)

        for check_group in cat_data["checks"]:
            group_title_html = (
                '<div style="background:linear-gradient(135deg,#f5af19 0%,#f12711 100%);'
                'padding:12px;border-radius:8px;margin-bottom:12px;margin-top:20px;">'
                '<div style="color:white;font-size:16px;font-weight:bold;">' + check_group["name"] + '</div>'
                '<div style="color:rgba(255,255,255,0.85);font-size:13px;margin-top:4px;">' + check_group["description"] + '</div></div>'
            )
            st.markdown(group_title_html, unsafe_allow_html=True)

            for item in check_group["items"]:
                if item["level"] == "必须检查":
                    level_bg = "#e74c3c"
                    level_color = "white"
                elif item["level"] == "推荐":
                    level_bg = "#f39c12"
                    level_color = "white"
                else:
                    level_bg = "#95a5a6"
                    level_color = "white"

                item_html = (
                    '<div style="background:white;border:1px solid #e0e0e0;border-radius:8px;'
                    'padding:12px;margin-bottom:8px;">'
                    '<div style="display:flex;align-items:flex-start;gap:8px;">'
                    '<input type="checkbox" style="margin-top:4px;width:16px;height:16px;cursor:pointer;">'
                    '<div style="flex:1;">'
                    '<div style="font-size:14px;color:#2c3e50;font-weight:500;margin-bottom:4px;">'
                    + item["check"] + '</div>'
                    '<div style="font-size:12px;color:#7f8c8d;line-height:1.5;">'
                    '💡 ' + item["tip"] + '</div>'
                    '</div>'
                    '<span style="font-size:11px;background:' + level_bg + ';color:' + level_color + ';'
                    'padding:2px 8px;border-radius:10px;white-space:nowrap;">' + item["level"] + '</span>'
                    '</div></div>'
                )
                st.markdown(item_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        **📋 使用说明：**
        - 🔴 **必须检查**：关键项，遗漏可能导致零件无法装配或功能失效
        - 🟡 **推荐**：建议项，可提高设计质量和可靠性
        - ☑️ 勾选每项检查内容，确保设计无遗漏
        """)

    # ==================== 内置材料库 + 过盈压装力计算 ====================
    with sub_tab5:
        from data.case_data import MATERIAL_PROPERTIES, MATERIAL_UNITS

        st.markdown("### 🔩 内置工程材料库")
        st.markdown("集成常用工程材料的物性参数，辅助热膨胀、过盈配合压装力等计算。")

        # 按类别分组显示
        categories = list(set(m["category"] for m in MATERIAL_PROPERTIES))
        selected_cat_mat = st.selectbox("按材料类别筛选", ["全部"] + sorted(categories))

        if selected_cat_mat == "全部":
            filtered_mats = MATERIAL_PROPERTIES
        else:
            filtered_mats = [m for m in MATERIAL_PROPERTIES if m["category"] == selected_cat_mat]

        mat_display = []
        for m in filtered_mats:
            mat_display.append({
                "材料": m["material"],
                "类别": m["category"],
                "密度(g/cm³)": m["density"],
                "弹性模量(GPa)": m["elastic_modulus"],
                "屈服强度(MPa)": m["yield_strength"],
                "抗拉强度(MPa)": m["tensile_strength"],
                "线膨胀系数(10⁻⁶/°C)": m["alpha"],
                "备注": m["note"],
            })

        mat_df = pd.DataFrame(mat_display)
        st.dataframe(mat_df, use_container_width=True, hide_index=True)

        # ==================== 过盈配合压装力计算 ====================
        st.markdown("---")
        st.markdown("### 🔧 过盈配合压装力计算")
        st.markdown("计算过盈配合件在压装时所需的轴向压力。**公式：P ≈ π × d × L × p × μ**")

        calc_col1, calc_col2, calc_col3 = st.columns(3)
        with calc_col1:
            shaft_material = st.selectbox("轴材料", [m["material"] for m in MATERIAL_PROPERTIES], index=2)
        with calc_col2:
            hole_material = st.selectbox("孔材料", [m["material"] for m in MATERIAL_PROPERTIES], index=0)
        with calc_col3:
            fit_class = st.selectbox("配合性质", ["轻度过盈", "中度过盈", "重度过盈"], index=1)

        calc_col4, calc_col5, calc_col6 = st.columns(3)
        with calc_col4:
            d = st.number_input("公称直径 d (mm)", value=50.0, min_value=1.0)
        with calc_col5:
            L = st.number_input("配合长度 L (mm)", value=60.0, min_value=1.0)
        with calc_col6:
            interference = st.number_input("过盈量 δ (mm)", value=0.03, min_value=0.001, step=0.001, format="%.4f")

        # 摩擦系数（材料组合）
        mu_values = {"轻度过盈": 0.08, "中度过盈": 0.12, "重度过盈": 0.15}
        mu = mu_values[fit_class]

        # 简化计算：压装力 P ≈ π × d × L × p_avg × μ
        # 其中 p_avg 为平均接触压力，简化取 过盈量/直径 × E_avg
        shaft_info = next(m for m in MATERIAL_PROPERTIES if m["material"] == shaft_material)
        hole_info = next(m for m in MATERIAL_PROPERTIES if m["material"] == hole_material)
        E_avg = (shaft_info["elastic_modulus"] + hole_info["elastic_modulus"]) / 2  # GPa
        p_avg = (interference / d) * E_avg * 1000  # MPa (换算)

        # 压装力 (kN)
        P = 3.14159 * d * L * p_avg * mu / 1000

        if st.button("计算压装力", type="primary", use_container_width=True):
            force_html = (
                '<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);'
                'padding:20px;border-radius:12px;color:white;margin-bottom:16px;text-align:center;">'
                '<div style="font-size:14px;opacity:0.9;">估算压装力</div>'
                '<div style="font-size:36px;font-weight:bold;margin-top:8px;">' + f'{P:.1f}' + ' kN</div>'
                '<div style="font-size:12px;opacity:0.8;margin-top:8px;">'
                '轴: ' + shaft_material + ' (E=' + str(shaft_info["elastic_modulus"]) + ' GPa) | '
                '孔: ' + hole_material + ' (E=' + str(hole_info["elastic_modulus"]) + ' GPa)</div></div>'
            )
            st.markdown(force_html, unsafe_allow_html=True)

            detail_html = (
                '<div style="background:white;border:1px solid #e0e0e0;border-radius:8px;padding:16px;">'
                '<div style="font-size:14px;color:#333;margin-bottom:12px;">'
                '<strong>计算参数：</strong><br>'
                '• 公称直径 d = ' + str(d) + ' mm<br>'
                '• 配合长度 L = ' + str(L) + ' mm<br>'
                '• 过盈量 δ = ' + str(interference) + ' mm<br>'
                '• 摩擦系数 μ = ' + str(mu) + ' (' + fit_class + ')<br>'
                '• 平均弹性模量 E = ' + f'{E_avg:.1f}' + ' GPa<br>'
                '• 平均接触压力 p = ' + f'{p_avg:.1f}' + ' MPa'
                '</div>'
                '<div style="font-size:14px;color:#333;">'
                '<strong>计算公式：</strong><br>'
                'P ≈ π × d × L × p × μ<br>'
                '= 3.1416 × ' + str(d) + ' × ' + str(L) + ' × ' + f'{p_avg:.1f}' + ' × ' + str(mu) + '<br>'
                '= <strong>' + f'{P:.1f}' + ' kN</strong>'
                '</div>'
                '<div style="font-size:12px;color:#666;margin-top:12px;background:#fff3cd;padding:8px;border-radius:4px;">'
                '💡 说明：本计算为简化估算，实际压装力受多种因素影响（零件硬度、温度、润滑条件、表面粗糙度等）。'
                '重度过盈配合建议采用加热孔或冷却轴的装配工艺。'
                '</div></div>'
            )
            st.markdown(detail_html, unsafe_allow_html=True)
