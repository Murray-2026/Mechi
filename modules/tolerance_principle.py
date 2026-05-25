"""公差原则计算模块 - 包容要求、最大/最小实体要求、补偿计算"""

def calculate_envelope_requirement(nominal_size, es, ei, geo_tol):
    """
    计算包容要求下的边界
    返回: 最大实体边界(MMB)、最小实体尺寸(LMS)
    """
    if es > ei:  # 孔
        mmc = nominal_size + ei  # 最小极限尺寸 = 最大实体尺寸
        lmc = nominal_size + es  # 最大极限尺寸 = 最小实体尺寸
        mmb = mmc  # 包容要求下，MMB = MMC
    else:  # 轴
        mmc = nominal_size + es  # 最大极限尺寸 = 最大实体尺寸
        lmc = nominal_size + ei  # 最小极限尺寸 = 最小实体尺寸
        mmb = mmc

    return {
        "mmc": round(mmc, 4),
        "lmc": round(lmc, 4),
        "mmb": round(mmb, 4),
        "tolerance_zone": round(abs(es - ei), 4),
        "geo_tol": geo_tol,
        "effective_geo_tol": 0,  # 包容要求下无补偿
        "description": "包容要求：实际表面不得超越最大实体边界(MMB)"
    }


def calculate_mmc_bonus(nominal_size, es, ei, geo_tol, actual_size=None):
    """
    计算最大实体要求(MMC)下的补偿值
    nominal_size: 公称尺寸
    es: 上偏差(孔为正，轴可为负)
    ei: 下偏差(孔可为负，轴为负)
    geo_tol: 给定几何公差值
    actual_size: 实际尺寸(可选，用于计算特定尺寸下的补偿)
    """
    if es > ei:  # 孔
        mmc = nominal_size + ei  # 最大实体尺寸(最小极限)
        lmc = nominal_size + es  # 最小实体尺寸(最大极限)
        if actual_size is None:
            actual_size = lmc  # 默认取最小实体状态
        deviation = actual_size - mmc  # 偏离MMC的量
    else:  # 轴
        mmc = nominal_size + es  # 最大实体尺寸(最大极限)
        lmc = nominal_size + ei  # 最小实体尺寸(最小极限)
        if actual_size is None:
            actual_size = lmc
        deviation = mmc - actual_size  # 偏离MMC的量

    bonus = max(0, deviation)
    effective_tol = geo_tol + bonus
    max_effective_tol = geo_tol + abs(mmc - lmc)

    return {
        "mmc": round(mmc, 4),
        "lmc": round(lmc, 4),
        "given_geo_tol": geo_tol,
        "bonus_tol": round(bonus, 4),
        "effective_geo_tol": round(effective_tol, 4),
        "max_effective_geo_tol": round(max_effective_tol, 4),
        "actual_size": round(actual_size, 4) if actual_size else None,
        "description": "最大实体要求：当实际尺寸偏离MMC时，几何公差可获得等于偏离量的补偿"
    }


def calculate_lmc_bonus(nominal_size, es, ei, geo_tol, actual_size=None):
    """
    计算最小实体要求(LMC)下的补偿值
    """
    if es > ei:  # 孔
        mmc = nominal_size + ei
        lmc = nominal_size + es  # 最小实体尺寸(最大极限)
        if actual_size is None:
            actual_size = mmc  # 默认取最大实体状态
        deviation = lmc - actual_size  # 偏离LMC的量
    else:  # 轴
        mmc = nominal_size + es
        lmc = nominal_size + ei  # 最小实体尺寸(最小极限)
        if actual_size is None:
            actual_size = mmc
        deviation = actual_size - lmc

    bonus = max(0, deviation)
    effective_tol = geo_tol + bonus
    max_effective_tol = geo_tol + abs(mmc - lmc)

    return {
        "lmc": round(lmc, 4),
        "mmc": round(mmc, 4),
        "given_geo_tol": geo_tol,
        "bonus_tol": round(bonus, 4),
        "effective_geo_tol": round(effective_tol, 4),
        "max_effective_geo_tol": round(max_effective_tol, 4),
        "actual_size": round(actual_size, 4) if actual_size else None,
        "description": "最小实体要求：当实际尺寸偏离LMC时，几何公差可获得等于偏离量的补偿"
    }


def render_tolerance_principle_tab():
    """渲染公差原则计算标签页"""
    import streamlit as st

    st.markdown("## 📐 公差原则计算器")
    st.markdown("基于 GB/T 4249-2009 / ASME Y14.5 标准，计算包容要求、最大/最小实体要求下的公差补偿")

    principle = st.selectbox("选择公差原则", [
        "包容要求 (E) - Envelope",
        "最大实体要求 (M) - MMC",
        "最小实体要求 (L) - LMC",
    ], index=0)

    col1, col2, col3 = st.columns(3)
    with col1:
        feature_type = st.selectbox("特征类型", ["孔(内表面)", "轴(外表面)"], index=0)
    with col2:
        nominal_size = st.number_input("公称尺寸 (mm)", value=50.0, min_value=0.1, max_value=5000.0)
    with col3:
        geo_tol = st.number_input("几何公差值 (mm)", value=0.025, min_value=0.001, max_value=10.0, format="%.4f")

    # 偏差输入
    if "孔" in feature_type:
        es = st.number_input("上偏差 ES (mm)", value=0.025, format="%.4f")
        ei = st.number_input("下偏差 EI (mm)", value=0.000, format="%.4f")
    else:
        es = st.number_input("上偏差 es (mm)", value=0.000, format="%.4f")
        ei = st.number_input("下偏差 ei (mm)", value=-0.016, format="%.4f")

    # 实际尺寸输入（仅MMC/LMC需要）
    actual_size = None
    if "最大实体" in principle or "最小实体" in principle:
        actual_size = st.number_input("实际尺寸 (mm)", value=None, min_value=0.0, format="%.4f",
                                       help="留空则计算最大补偿量")

    # 计算
    if st.button("计算", type="primary", use_container_width=True):
        if "包容" in principle:
            result = calculate_envelope_requirement(nominal_size, es, ei, geo_tol)
        elif "最大实体" in principle:
            result = calculate_mmc_bonus(nominal_size, es, ei, geo_tol, actual_size)
        else:
            result = calculate_lmc_bonus(nominal_size, es, ei, geo_tol, actual_size)

        # 显示结果
        st.markdown("---")
        st.markdown("### 📊 计算结果")

        # 结果卡片
        result_html = (
            '<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);'
            'padding:16px;border-radius:8px;margin-bottom:12px;">'
            '<div style="color:white;font-size:16px;font-weight:bold;margin-bottom:8px;">'
            + principle + '</div>'
            '<div style="color:rgba(255,255,255,0.9);font-size:13px;">'
            + result["description"] + '</div></div>'
        )
        st.markdown(result_html, unsafe_allow_html=True)

        # 详细数据
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if "mmc" in result:
                st.metric("最大实体尺寸 MMC", str(result["mmc"]) + " mm")
            if "lmc" in result:
                st.metric("最小实体尺寸 LMC", str(result["lmc"]) + " mm")
        with col_b:
            st.metric("给定几何公差", str(result.get("given_geo_tol", geo_tol)) + " mm")
            if "bonus_tol" in result:
                st.metric("补偿公差", str(result["bonus_tol"]) + " mm")
        with col_c:
            st.metric("有效公差", str(result["effective_geo_tol"]) + " mm")
            if "max_effective_geo_tol" in result:
                st.metric("最大有效公差", str(result["max_effective_geo_tol"]) + " mm")

        # 解释
        with st.expander("📖 计算说明", expanded=True):
            if "包容" in principle:
                st.markdown("""
                **包容要求**要求被测要素的实际轮廓不得超越最大实体边界(MMB)。

                - 最大实体边界 = 最大实体尺寸 = MMC
                - 局部实际尺寸不得超出最小实体尺寸 = LMC
                - 包容要求下几何公差无补偿，始终为给定值
                - 适用于需要保证配合性质的场合
                """)
            elif "最大实体" in principle:
                bonus = result["bonus_tol"]
                st.markdown("""
                **最大实体要求(MMC)**允许在尺寸偏离MMC时，将偏离量补偿给几何公差。

                - 补偿量 = |实际尺寸 - MMC|
                - 有效公差 = 给定公差 + 补偿量
                - 最大有效公差 = 给定公差 + 尺寸公差
                - 当前补偿量：**""" + str(bonus) + """ mm**
                - 当前有效公差：**""" + str(result["effective_geo_tol"]) + """ mm**

                💡 这意味着实际加工精度可以适当放宽，降低了制造成本，同时仍保证装配互换性。
                """)
            else:
                st.markdown("""
                **最小实体要求(LMC)**允许在尺寸偏离LMC时，将偏离量补偿给几何公差。

                - 补偿量 = |LMC - 实际尺寸|
                - 有效公差 = 给定公差 + 补偿量
                - 适用于需要保证最小壁厚的场合
                """)
