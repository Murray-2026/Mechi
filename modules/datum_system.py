"""基准体系定义模块 - 支持主/次/三级基准模拟"""

def generate_datum_system_svg(datum_a_type, datum_b_type, datum_c_type,
                               feature_type, tolerance_value):
    """生成基准体系示意图SVG"""
    # 根据基准类型和被测特征生成SVG
    svg_width = 700
    svg_height = 400

    svg = '<svg width="' + str(svg_width) + '" height="' + str(svg_height) + '" xmlns="http://www.w3.org/2000/svg">'

    # 背景网格
    svg += '<defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">'
    svg += '<path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f0f0f0" stroke-width="0.5"/>'
    svg += '</pattern></defs>'
    svg += '<rect width="100%" height="100%" fill="url(#grid)"/>'

    # 绘制零件轮廓（简化矩形）
    svg += '<rect x="100" y="80" width="400" height="240" rx="4" fill="#e8f4fd" stroke="#2196F3" stroke-width="2"/>'

    # 绘制基准A（主基准 - 底面）
    if datum_a_type:
        svg += '<rect x="100" y="320" width="400" height="30" rx="2" fill="#FFCDD2" stroke="#F44336" stroke-width="1.5"/>'
        svg += '<line x1="300" y1="350" x2="300" y2="380" stroke="#333" stroke-width="2"/>'
        svg += '<polygon points="300,380 294,370 306,370" fill="#333"/>'
        svg += '<rect x="286" y="382" width="28" height="16" rx="2" fill="none" stroke="#333" stroke-width="1.5"/>'
        svg += '<text x="300" y="395" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">A</text>'
        svg += '<text x="300" y="340" text-anchor="middle" font-size="11" fill="#F44336">主基准 (第一基准)</text>'

    # 绘制基准B（次基准 - 侧面）
    if datum_b_type:
        svg += '<rect x="500" y="80" width="30" height="240" rx="2" fill="#C8E6C9" stroke="#4CAF50" stroke-width="1.5"/>'
        svg += '<line x1="530" y1="200" x2="560" y2="200" stroke="#333" stroke-width="2"/>'
        svg += '<polygon points="560,200 550,194 550,206" fill="#333"/>'
        svg += '<rect x="562" y="186" width="28" height="16" rx="2" fill="none" stroke="#333" stroke-width="1.5"/>'
        svg += '<text x="576" y="199" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">B</text>'
        svg += '<text x="515" y="200" text-anchor="middle" font-size="11" fill="#4CAF50" transform="rotate(90,515,200)">次基准</text>'

    # 绘制基准C（第三基准 - 另一侧面）
    if datum_c_type:
        svg += '<rect x="70" y="80" width="30" height="240" rx="2" fill="#FFF9C4" stroke="#FFC107" stroke-width="1.5"/>'
        svg += '<line x1="70" y1="200" x2="40" y2="200" stroke="#333" stroke-width="2"/>'
        svg += '<polygon points="40,200 50,194 50,206" fill="#333"/>'
        svg += '<rect x="12" y="186" width="28" height="16" rx="2" fill="none" stroke="#333" stroke-width="1.5"/>'
        svg += '<text x="26" y="199" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">C</text>'

    # 绘制被测特征（孔）
    if feature_type == "孔":
        svg += '<circle cx="300" cy="200" r="30" fill="#fff" stroke="#9C27B0" stroke-width="2" stroke-dasharray="5,3"/>'
        svg += '<circle cx="300" cy="200" r="15" fill="#E1BEE7" stroke="#9C27B0" stroke-width="1"/>'
        svg += '<line x1="300" y1="170" x2="300" y2="140" stroke="#9C27B0" stroke-width="1.5"/>'
        svg += '<polygon points="300,140 296,148 304,148" fill="#9C27B0"/>'
        svg += '<text x="300" y="130" text-anchor="middle" font-size="11" fill="#9C27B0">被测孔</text>'

    # 公差框格
    svg += '<rect x="150" y="30" width="300" height="30" rx="2" fill="white" stroke="#333" stroke-width="1.5"/>'
    svg += '<line x1="250" y1="30" x2="250" y2="60" stroke="#333" stroke-width="1"/>'
    svg += '<line x1="350" y1="30" x2="350" y2="60" stroke="#333" stroke-width="1"/>'
    svg += '<line x1="450" y1="30" x2="450" y2="60" stroke="#333" stroke-width="1"/>'

    svg += '<text x="200" y="50" text-anchor="middle" font-size="11" fill="#333">' + feature_type + '</text>'
    svg += '<text x="300" y="50" text-anchor="middle" font-size="11" fill="#333">' + str(tolerance_value) + '</text>'

    datum_labels = ""
    if datum_a_type:
        datum_labels += '<text x="400" y="50" text-anchor="middle" font-size="11" fill="#F44336">A</text>'
    if datum_b_type:
        svg += '<line x1="450" y1="30" x2="450" y2="60" stroke="#333" stroke-width="1"/>'
        datum_labels += '<text x="475" y="50" text-anchor="middle" font-size="11" fill="#4CAF50">B</text>'
    if datum_c_type:
        svg += '<line x1="500" y1="30" x2="500" y2="60" stroke="#333" stroke-width="1"/>'
        datum_labels += '<text x="525" y="50" text-anchor="middle" font-size="11" fill="#FFC107">C</text>'

    svg += datum_labels

    # 图例
    svg += '<rect x="560" y="80" width="120" height="100" rx="4" fill="white" stroke="#ddd" stroke-width="1"/>'
    svg += '<text x="620" y="96" text-anchor="middle" font-size="10" font-weight="bold">图例</text>'
    svg += '<rect x="570" y="102" width="10" height="10" fill="#FFCDD2" stroke="#F44336" stroke-width="0.5"/>'
    svg += '<text x="585" y="111" font-size="9" fill="#333">主基准 A</text>'
    svg += '<rect x="570" y="118" width="10" height="10" fill="#C8E6C9" stroke="#4CAF50" stroke-width="0.5"/>'
    svg += '<text x="585" y="127" font-size="9" fill="#333">次基准 B</text>'
    svg += '<rect x="570" y="134" width="10" height="10" fill="#FFF9C4" stroke="#FFC107" stroke-width="0.5"/>'
    svg += '<text x="585" y="143" font-size="9" fill="#333">第三基准 C</text>'
    svg += '<circle cx="575" cy="160" r="5" fill="none" stroke="#9C27B0" stroke-width="1" stroke-dasharray="2,1"/>'
    svg += '<text x="585" y="163" font-size="9" fill="#333">被测特征</text>'

    svg += '</svg>'
    return svg


def render_datum_system_tab():
    """渲染基准体系定义标签页"""
    import streamlit as st

    st.markdown("## &#x1F4D0; 基准体系定义与模拟")
    st.info("""
    &#x1F4A1; 基准是确定被测要素方向或位置的理想要素。三基面体系由三个相互垂直的基准平面组成，
    分别限制工件的6个自由度。基准的顺序（A&#x2192;B&#x2192;C）非常重要，第一基准限制的自由度最多。
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        datum_a = st.selectbox("主基准 A（第一基准）",
            ["平面（底面）", "圆柱面（轴线）", "无"], index=0,
            help="限制3个自由度（平面）或2个自由度（圆柱面）")
    with col2:
        datum_b = st.selectbox("次基准 B（第二基准）",
            ["平面（侧面）", "圆柱面（轴线）", "无"], index=0,
            help="限制2个自由度（平面）或1个自由度（圆柱面）")
    with col3:
        datum_c = st.selectbox("第三基准 C",
            ["平面（端面）", "圆柱面（轴线）", "无"], index=0,
            help="限制1个自由度")

    col4, col5 = st.columns(2)
    with col4:
        feature_type = st.selectbox("被测特征类型",
            ["位置度", "垂直度", "平行度", "倾斜度", "同轴度"], index=0)
    with col5:
        tol_val = st.number_input("公差值 (mm)", value=0.05, min_value=0.001, max_value=10.0, step=0.001, format="%.3f")

    # 生成示意图
    svg = generate_datum_system_svg(
        datum_a != "无", datum_b != "无", datum_c != "无",
        feature_type, tol_val
    )
    st.markdown(svg, unsafe_allow_html=True)

    # 基准说明
    st.markdown("### &#x1F4CB; 基准体系说明")

    if datum_a != "无":
        st.markdown("""
        **&#x1F534; 主基准 A**（第一基准）
        - 限制自由度最多（3个：1个移动 + 2个旋转）
        - 应选择最大的、最稳定的定位面
        - 是加工和检测的首要参考
        """)

    if datum_b != "无":
        st.markdown("""
        **&#x1F7E2; 次基准 B**（第二基准）
        - 垂直于基准A，限制2个自由度
        - 应选择次大的定位面
        - 在基准A已定位的基础上进一步约束
        """)

    if datum_c != "无":
        st.markdown("""
        **&#x1F7E1; 第三基准 C**
        - 垂直于基准A和B，限制1个自由度
        - 完全定位工件
        - 通常选择最小的定位面
        """)

    # 自由度分析
    with st.expander("&#x1F527; 自由度分析", expanded=False):
        total_dof = 6
        if datum_a != "无": total_dof -= 3
        if datum_b != "无": total_dof -= 2
        if datum_c != "无": total_dof -= 1

        st.markdown("""
        | 基准 | 限制的自由度 | 剩余自由度 |
        |------|------------|------------|
        | 初始 | — | 6（完全自由） |
        """ + (("| A（主基准） | 3个 | 3个 |" if datum_a != "无" else "") +
            ("| B（次基准） | 2个 | 1个 |" if datum_b != "无" else "") +
            ("| C（第三基准） | 1个 | 0个（完全约束） |" if datum_c != "无" else ""))
        )
