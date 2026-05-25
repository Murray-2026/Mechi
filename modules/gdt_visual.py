"""GD&T符号交互式可视化模块 - ASME Y14.5 / GB/T 1182"""

def generate_gdt_interactive_card(symbol_data, index):
    """生成单个GD&T符号的交互式卡片HTML"""
    name_cn = symbol_data["name_cn"]
    name_en = symbol_data["name_en"]
    symbol = symbol_data["symbol"]
    category = symbol_data["category"]
    needs_datum = symbol_data["needs_datum"]
    tolerance_zone = symbol_data["tolerance_zone"]
    description = symbol_data["description"]
    inspection_method = symbol_data["inspection_method"]
    application = symbol_data["application"]
    hover_explain = symbol_data["hover_explain"]
    asme_clause = symbol_data.get("asme_clause", "")

    datum_badge = "需要基准" if needs_datum else "无基准"
    datum_color = "#e74c3c" if needs_datum else "#27ae60"

    # 分类颜色
    cat_colors = {
        "形状公差": "#3498db",
        "定向公差": "#e67e22",
        "定位公差": "#9b59b6",
        "跳动公差": "#e74c3c",
        "轮廓公差": "#1abc9c",
    }
    cat_color = cat_colors.get(category, "#95a5a6")

    asme_badge = ('<span style="font-size:11px;background:#ecf0f1;color:#7f8c8d;'
                  'padding:2px 8px;border-radius:10px;">ASME ' + asme_clause + '</span>'
                  if asme_clause else '')

    html = (
        '<div class="gdt-card" style="background:white; border-radius:12px; '
        'box-shadow:0 2px 8px rgba(0,0,0,0.1); padding:20px; margin-bottom:16px; '
        'border-left:4px solid ' + cat_color + '; transition:all 0.3s ease; '
        'position:relative;" '
        'onmouseover="this.style.boxShadow=\'0 4px 16px rgba(0,0,0,0.2)\';'
        'this.style.transform=\'translateY(-2px)\'" '
        'onmouseout="this.style.boxShadow=\'0 2px 8px rgba(0,0,0,0.1)\';'
        'this.style.transform=\'translateY(0)\'">'

        # 头部：符号+名称+分类
        '<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">'
        '<div style="width:56px;height:56px;border-radius:12px;background:' + cat_color + '15;'
        'display:flex;align-items:center;justify-content:center;font-size:28px;'
        'border:2px solid ' + cat_color + '30;" title="' + hover_explain + '">'
        + symbol + '</div>'
        '<div style="flex:1;">'
        '<div style="font-size:18px;font-weight:bold;color:#2c3e50;">' + name_cn
        + ' <span style="font-size:13px;color:#7f8c8d;font-weight:normal;">'
        + name_en + '</span></div>'
        '<div style="display:flex;gap:6px;margin-top:4px;">'
        '<span style="font-size:11px;background:' + cat_color + '20;color:' + cat_color + ';'
        'padding:2px 8px;border-radius:10px;">' + category + '</span>'
        '<span style="font-size:11px;background:' + datum_color + '20;color:' + datum_color + ';'
        'padding:2px 8px;border-radius:10px;">' + datum_badge + '</span>'
        + asme_badge
        + '</div></div></div>'

        # 悬停解释区域
        '<div class="gdt-hover-info" style="background:#f8f9fa;border-radius:8px;padding:12px;'
        'margin-bottom:12px;border:1px solid #e8ecf1;">'
        '<div style="font-size:12px;color:#5f6368;margin-bottom:4px;font-weight:bold;">'
        '&#x1F4A1; 详细解释</div>'
        '<div style="font-size:13px;color:#333;line-height:1.6;">'
        + hover_explain + '</div></div>'

        # 详细信息网格
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">'
        '<div style="background:#f0f7ff;padding:10px;border-radius:6px;">'
        '<div style="font-size:11px;color:#5f6368;">&#x1F4D0; 公差带</div>'
        '<div style="font-size:12px;color:#333;margin-top:2px;">'
        + tolerance_zone + '</div></div>'
        '<div style="background:#f0fff4;padding:10px;border-radius:6px;">'
        '<div style="font-size:11px;color:#5f6368;">&#x1F52C; 检测方法</div>'
        '<div style="font-size:12px;color:#333;margin-top:2px;">'
        + inspection_method + '</div></div>'
        '<div style="background:#fff8f0;padding:10px;border-radius:6px;grid-column:span 2;">'
        '<div style="font-size:11px;color:#5f6368;">&#x1F3ED; 典型应用</div>'
        '<div style="font-size:12px;color:#333;margin-top:2px;">'
        + application + '</div></div>'
        '</div></div>'
    )
    return html


def render_gdt_visual_tab():
    """渲染GD&T交互式可视化标签页"""
    import streamlit as st
    from data.asme_data import ASME_GDT_SYMBOLS, ASME_VS_GB_COMPARISON, ASME_MODIFIERS

    st.markdown("## &#x1F3AF; GD&T 符号交互式图解")
    st.markdown("基于 ASME Y14.5-2018 / GB/T 1182-2018 标准，悬停查看详细解释")

    # 分类筛选
    categories = ["全部"] + list(set(s["category"] for s in ASME_GDT_SYMBOLS))
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_cat = st.selectbox("分类筛选", categories, index=0)
    with col2:
        search_gdt = st.text_input("搜索GD&T符号", placeholder="输入中文名称如：直线度、圆度、位置度...", key="gdt_visual_search")

    # 过滤
    filtered = ASME_GDT_SYMBOLS
    if selected_cat != "全部":
        filtered = [s for s in filtered if s["category"] == selected_cat]
    if search_gdt:
        filtered = [s for s in filtered if search_gdt in s["name_cn"] or search_gdt.lower() in s["name_en"].lower()]

    # 渲染卡片
    for i, sym in enumerate(filtered):
        card_html = generate_gdt_interactive_card(sym, i)
        st.markdown(card_html, unsafe_allow_html=True)

    # ASME vs GB 对照表
    with st.expander("&#x1F4CA; ASME Y14.5 vs GB/T 1182 对照表", expanded=False):
        import pandas as pd
        df_compare = pd.DataFrame(ASME_VS_GB_COMPARISON)
        st.dataframe(df_compare, use_container_width=True, hide_index=True)

    # ASME修饰符
    with st.expander("&#x1F527; ASME Y14.5 修饰符说明", expanded=False):
        for mod in ASME_MODIFIERS:
            mod_html = (
                '<div style="background:white;border-radius:8px;padding:12px;margin-bottom:8px;'
                'border:1px solid #e0e0e0;">'
                '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
                '<span style="font-size:24px;">' + mod["symbol"] + '</span>'
                '<span style="font-size:16px;font-weight:bold;">' + mod["name"] + '</span>'
                '<span style="font-size:12px;color:#7f8c8d;">' + mod["name_en"] + '</span></div>'
                '<div style="font-size:13px;color:#333;margin-bottom:4px;">' + mod["description"] + '</div>'
                '<div style="font-size:12px;color:#5f6368;">GB对应：' + mod["gb_equivalent"] + '</div></div>'
            )
            st.markdown(mod_html, unsafe_allow_html=True)
