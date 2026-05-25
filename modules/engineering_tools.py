"""工程工具模块 - 成本关联、热膨胀计算、表面粗糙度推荐"""

def render_engineering_tools_tab():
    """渲染工程工具标签页"""
    import streamlit as st
    from data.cost_process_data import (
        TOLERANCE_COST_DATA, PROCESS_PRECISION,
        THERMAL_EXPANSION_DATA, SURFACE_ROUGHNESS_DATA
    )
    import pandas as pd

    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "💰 公差等级-成本关联", "🌡️ 热膨胀计算", "🔲 表面粗糙度推荐", "🛡️ 防错检查清单"
    ])

    # ==================== 公差等级-成本关联 ====================
    with sub_tab1:
        st.markdown("### 💰 公差等级-成本关联")
        st.markdown("公差等级直接影响制造成本。了解成本关联有助于在精度与经济性之间做出平衡。")

        # 成本对比表
        st.markdown("#### 公差等级成本指数对比")
        cost_df = pd.DataFrame([
            {"等级": k, "成本指数": v["cost_index"], "相对成本": v["relative_cost"],
             "相邻等级成本增幅": v["cost_increase"], "典型工艺": v["typical_process"]}
            for k, v in TOLERANCE_COST_DATA.items()
        ])
        st.dataframe(cost_df, use_container_width=True, hide_index=True)

        # 成本可视化提示
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

        # 加工工艺精度范围
        with st.expander("🔧 常用加工工艺经济精度范围", expanded=True):
            process_df = pd.DataFrame(PROCESS_PRECISION)
            st.dataframe(process_df, use_container_width=True, hide_index=True)

    # ==================== 热膨胀计算 ====================
    with sub_tab2:
        st.markdown("### 🌡️ 热膨胀系数查询与计算")
        st.markdown("计算温度变化导致的尺寸变化：**ΔL = α × L × ΔT**")

        # 材料选择
        materials = [m["material"] for m in THERMAL_EXPANSION_DATA]
        selected_material = st.selectbox("选择材料", materials, index=4)

        # 获取材料数据
        material_data = next(m for m in THERMAL_EXPANSION_DATA if m["material"] == selected_material)

        # 材料信息卡片
        mat_html = (
            '<div style="background:#fff3e0;border:1px solid #ffb74d;border-radius:8px;padding:12px;margin-bottom:12px;">'
            '<div style="font-size:16px;font-weight:bold;color:#e65100;">' + material_data["material"] + '</div>'
            '<div style="font-size:14px;color:#333;">热膨胀系数 α = <b>' + str(material_data["coefficient"]) + ' × 10⁻⁶/°C</b></div>'
            '<div style="font-size:12px;color:#666;">适用温度范围：' + material_data["range"] + '</div>'
            '<div style="font-size:12px;color:#666;">' + material_data["note"] + '</div></div>'
        )
        st.markdown(mat_html, unsafe_allow_html=True)

        # 计算参数
        col1, col2, col3 = st.columns(3)
        with col1:
            L = st.number_input("原始长度 L (mm)", value=100.0, min_value=0.01)
        with col2:
            T1 = st.number_input("初始温度 (°C)", value=20.0)
        with col3:
            T2 = st.number_input("最终温度 (°C)", value=100.0)

        if st.button("计算尺寸变化", type="primary", use_container_width=True):
            alpha = material_data["coefficient"] * 1e-6  # 转换为 /°C
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
                '💡 提示：在精密配合设计中，应考虑热膨胀导致的尺寸变化，预留合理的配合间隙。</div></div>'
            )
            st.markdown(result_html, unsafe_allow_html=True)

        # 材料对比表
        with st.expander("📊 常用材料热膨胀系数对比", expanded=False):
            thermal_df = pd.DataFrame(THERMAL_EXPANSION_DATA)
            st.dataframe(thermal_df, use_container_width=True, hide_index=True)

    # ==================== 表面粗糙度推荐 ====================
    with sub_tab3:
        st.markdown("### 🔲 表面粗糙度关联推荐")
        st.markdown("表面粗糙度与加工工艺、成本密切相关。选择合适的粗糙度等级是平衡精度与成本的关键。")

        # 粗糙度选择
        selected_ra = st.selectbox("选择粗糙度等级 Ra (μm)",
            [str(r["ra_value"]) for r in SURFACE_ROUGHNESS_DATA], index=4)
        ra_data = next(r for r in SURFACE_ROUGHNESS_DATA if str(r["ra_value"]) == selected_ra)

        # 粗糙度信息卡片
        ra_html = (
            '<div style="background:linear-gradient(135deg,#a8e063 0%,#56ab2f 100%);'
            'padding:16px;border-radius:8px;color:white;margin-bottom:12px;">'
            '<div style="font-size:20px;font-weight:bold;">Ra ' + selected_ra + ' μm (' + ra_data["grade"] + ')</div>'
            '<div style="font-size:14px;margin-top:8px;">推荐加工工艺：' + ra_data["process"] + '</div>'
            '<div style="font-size:14px;margin-top:4px;">典型应用：' + ra_data["application"] + '</div>'
            '<div style="font-size:14px;margin-top:4px;">' + ra_data["cost_note"] + '</div></div>'
        )
        st.markdown(ra_html, unsafe_allow_html=True)

        # 完整粗糙度表
        with st.expander("📊 表面粗糙度等级对照表", expanded=True):
            ra_df = pd.DataFrame(SURFACE_ROUGHNESS_DATA)
            st.dataframe(ra_df, use_container_width=True, hide_index=True)

    # ==================== 防错设计检查清单 ====================
    with sub_tab4:
        from data.case_data import POKAYOKE_CHECKLIST

        st.markdown("### 🛡️ 防错设计检查清单")
        st.markdown("帮助工程师在设计阶段排查常见错误，涵盖对称性、装配防错、公差标注、工艺可行性等方面。")

        # 分类选择
        category_names = [cat["icon"] + " " + cat["category"] for cat in POKAYOKE_CHECKLIST]
        selected_cat = st.selectbox("选择检查类别", category_names, index=0)

        cat_data = next(cat for cat in POKAYOKE_CHECKLIST if cat["icon"] + " " + cat["category"] == selected_cat)

        for check_group in cat_data["checks"]:
            # 检查组标题
            group_title_html = (
                '<div style="background:linear-gradient(135deg,#f5af19 0%,#f12711 100%);'
                'padding:12px;border-radius:8px;margin-bottom:12px;margin-top:20px;">'
                '<div style="color:white;font-size:16px;font-weight:bold;">' + check_group["name"] + '</div>'
                '<div style="color:rgba(255,255,255,0.85);font-size:13px;margin-top:4px;">' + check_group["description"] + '</div></div>'
            )
            st.markdown(group_title_html, unsafe_allow_html=True)

            # 检查项列表
            for item in check_group["items"]:
                # 等级标签颜色
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

        # 使用说明
        st.markdown("---")
        st.markdown("""
        **📋 使用说明：**
        - 🔴 **必须检查**：关键项，遗漏可能导致零件无法装配或功能失效
        - 🟡 **推荐**：建议项，可提高设计质量和可靠性
        - ☑️ 勾选每项检查内容，确保设计无遗漏
        - 建议在图纸评审前逐项核对
        """)
