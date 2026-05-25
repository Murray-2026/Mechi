# ASME Y14.5-2018 GD&T标准数据

# GD&T符号定义（14个公差控制符号）
ASME_GDT_SYMBOLS = [
    {
        "name_cn": "直线度", "name_en": "Straightness", "symbol": "—",
        "category": "形状公差", "needs_datum": False,
        "feature_type": "单一要素",
        "tolerance_zone": "两平行直线之间的区域",
        "description": "控制线要素的直度误差。应用于表面素线、轴线或平面内的线。",
        "asme_clause": "6.4.1",
        "inspection_method": "刀口尺、平尺、自准直仪",
        "application": "导轨面、轴心线、刀具刃口",
        "hover_explain": "直线度公差控制被测直线要素对其理想直线的偏差。公差带为两平行直线间的区域，宽度等于公差值t。"
    },
    {
        "name_cn": "平面度", "name_en": "Flatness", "symbol": "▱",
        "category": "形状公差", "needs_datum": False,
        "feature_type": "单一要素",
        "tolerance_zone": "两平行平面之间的区域",
        "description": "控制平面的平整度误差。公差带为两平行平面之间的区域。",
        "asme_clause": "6.4.2",
        "inspection_method": "平板、三坐标测量机、水平仪",
        "application": "密封面、安装基面、工作台面",
        "hover_explain": "平面度公差控制被测平面对其理想平面的偏差。公差带为两平行平面间的区域，间距等于公差值t。"
    },
    {
        "name_cn": "圆度", "name_en": "Circularity", "symbol": "○",
        "category": "形状公差", "needs_datum": False,
        "feature_type": "单一要素",
        "tolerance_zone": "两同心圆之间的区域",
        "description": "控制回转体横截面的形状误差。公差带为两同心圆之间的区域。",
        "asme_clause": "6.4.3",
        "inspection_method": "圆度仪、V形块+百分表",
        "application": "轴承配合面、活塞、气缸内孔",
        "hover_explain": "圆度公差控制被测回转体横截面对其理想圆的偏差。公差带为两同心圆间的区域，半径差等于公差值t。"
    },
    {
        "name_cn": "圆柱度", "name_en": "Cylindricity", "symbol": "⌭",
        "category": "形状公差", "needs_datum": False,
        "feature_type": "单一要素",
        "tolerance_zone": "两同轴圆柱面之间的区域",
        "description": "综合控制圆柱体横截面和纵截面的形状误差。",
        "asme_clause": "6.4.4",
        "inspection_method": "圆度仪+轴向移动、三坐标测量机",
        "application": "精密轴颈、液压缸筒、定位销",
        "hover_explain": "圆柱度公差综合控制被测圆柱面的圆度、素线直线度和轴线直线度。公差带为两同轴圆柱面间的区域，半径差等于公差值t。"
    },
    {
        "name_cn": "平行度", "name_en": "Parallelism", "symbol": "∥",
        "category": "定向公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "平行于基准的两平行平面/直线之间的区域",
        "description": "控制被测要素相对于基准的平行程度。",
        "asme_clause": "6.5.1",
        "inspection_method": "平板+百分表、三坐标测量机",
        "application": "导轨平行面、轴承孔中心线、箱体结合面",
        "hover_explain": "平行度公差控制被测要素相对于基准要素的平行方向偏差。公差带为平行于基准的两平行平面/直线间的区域，宽度等于公差值t。"
    },
    {
        "name_cn": "垂直度", "name_en": "Perpendicularity", "symbol": "⊥",
        "category": "定向公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "垂直于基准的两平行平面/直线之间的区域",
        "description": "控制被测要素相对于基准的垂直程度。",
        "asme_clause": "6.5.2",
        "inspection_method": "直角尺、三坐标测量机、光学直角仪",
        "application": "轴肩端面、箱体侧面、定位面",
        "hover_explain": "垂直度公差控制被测要素相对于基准要素的90°方向偏差。公差带为垂直于基准的两平行平面/直线间的区域，宽度等于公差值t。"
    },
    {
        "name_cn": "倾斜度", "name_en": "Angularity", "symbol": "∠",
        "category": "定向公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "与基准成理论正确角度的两平行平面之间的区域",
        "description": "控制被测要素相对于基准的倾斜角度误差。",
        "asme_clause": "6.5.3",
        "inspection_method": "正弦规、三坐标测量机、万能角度尺",
        "application": "斜面、锥面、楔形件",
        "hover_explain": "倾斜度公差控制被测要素相对于基准要素在给定角度方向的偏差。公差带为与基准成理论正确角度的两平行平面间的区域。"
    },
    {
        "name_cn": "位置度", "name_en": "Position", "symbol": "⌖",
        "category": "定位公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "圆柱面/球面/两平行平面内的区域",
        "description": "控制被测要素的实际位置对其理想位置的偏差。最常用的GD&T符号之一。",
        "asme_clause": "6.6.1",
        "inspection_method": "功能量规、三坐标测量机",
        "application": "螺栓孔组、销孔组、轴承座孔",
        "hover_explain": "位置度公差控制被测要素（点、线、面）的实际位置对其理想位置的偏差。对于孔，公差带为直径等于公差值φt的圆柱面内的区域，轴线位于理想位置。"
    },
    {
        "name_cn": "同轴度", "name_en": "Concentricity", "symbol": "◎",
        "category": "定位公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "与基准同轴的圆柱面内的区域",
        "description": "控制被测轴线对基准轴线的同轴程度。ASME Y14.5-2018中已不推荐使用，建议用位置度替代。",
        "asme_clause": "6.6.2",
        "inspection_method": "V形块+百分表、三坐标测量机",
        "application": "阶梯轴、套筒类零件",
        "hover_explain": "同轴度公差控制被测轴线对基准轴线的同轴偏差。公差带为与基准同轴的圆柱面内的区域，直径等于公差值φt。注意：ASME Y14.5-2018建议用位置度替代同轴度。"
    },
    {
        "name_cn": "对称度", "name_en": "Symmetry", "symbol": "⌢",
        "category": "定位公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "对称配置于基准中心平面两侧的两平行平面之间的区域",
        "description": "控制被测中心要素对基准中心平面的对称程度。ASME Y14.5-2018中已不推荐使用。",
        "asme_clause": "6.6.3",
        "inspection_method": "V形块+百分表、三坐标测量机",
        "application": "键槽、花键、对称结构",
        "hover_explain": "对称度公差控制被测中心要素对基准中心平面的对称偏差。公差带为对称配置于基准中心平面两侧的两平行平面间的区域，宽度等于公差值t。"
    },
    {
        "name_cn": "圆跳动", "name_en": "Circular Runout", "symbol": "↗",
        "category": "跳动公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "任意测量平面内两同心圆之间的区域",
        "description": "综合控制圆度、同轴度等误差。测量时零件旋转一周。",
        "asme_clause": "6.7.1",
        "inspection_method": "V形块+百分表、两顶尖+百分表",
        "application": "旋转轴、齿轮轴颈、电机轴",
        "hover_explain": "圆跳动公差是综合公差，控制被测要素绕基准轴线旋转一周时，在任意测量平面内的径向/轴向/斜向跳动量。公差带为两同心圆间的区域，半径差等于公差值t。"
    },
    {
        "name_cn": "全跳动", "name_en": "Total Runout", "symbol": "⇗",
        "category": "跳动公差", "needs_datum": True,
        "feature_type": "关联要素",
        "tolerance_zone": "两同轴圆柱面/两平行平面之间的区域",
        "description": "综合控制圆柱度、同轴度等误差。测量时零件连续旋转并轴向移动。",
        "asme_clause": "6.7.2",
        "inspection_method": "两顶尖+百分表（连续移动）",
        "application": "精密主轴、高速旋转部件",
        "hover_explain": "全跳动公差是综合公差，控制被测要素绕基准轴线连续旋转时，在整个测量面上的跳动量。径向全跳动可同时控制圆柱度和同轴度。"
    },
    {
        "name_cn": "轮廓度（线）", "name_en": "Profile of a Line", "symbol": "⌒",
        "category": "轮廓公差", "needs_datum": False,
        "feature_type": "单一/关联要素",
        "tolerance_zone": "沿理想轮廓等距分布的两等距曲线之间的区域",
        "description": "控制任意截面轮廓的形状误差。",
        "asme_clause": "6.3.1",
        "inspection_method": "轮廓样板、三坐标测量机",
        "application": "凸轮轮廓、叶片截面、模具型面",
        "hover_explain": "线轮廓度公差控制被测轮廓线对其理想轮廓的偏差。公差带为沿理想轮廓法向等距分布的两等距曲线间的区域，宽度等于公差值t。"
    },
    {
        "name_cn": "轮廓度（面）", "name_en": "Profile of a Surface", "symbol": "⌓",
        "category": "轮廓公差", "needs_datum": False,
        "feature_type": "单一/关联要素",
        "tolerance_zone": "沿理想轮廓等距分布的两等距曲面之间的区域",
        "description": "控制三维曲面的形状误差。",
        "asme_clause": "6.3.2",
        "inspection_method": "三坐标测量机、光学扫描",
        "application": "复杂曲面、汽车车身面板、叶片",
        "hover_explain": "面轮廓度公差控制被测曲面对其理想曲面的偏差。公差带为沿理想曲面法向等距分布的两等距曲面间的区域，宽度等于公差值t。"
    },
]

# ASME与ISO/GB对照表
ASME_VS_GB_COMPARISON = [
    {"asme": "Straightness", "gb": "直线度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Flatness", "gb": "平面度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Circularity", "gb": "圆度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Cylindricity", "gb": "圆柱度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Parallelism", "gb": "平行度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Perpendicularity", "gb": "垂直度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Angularity", "gb": "倾斜度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Position", "gb": "位置度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Concentricity", "gb": "同轴度", "gb_standard": "GB/T 1182-2018", "note": "ASME 2018不推荐使用，建议用Position"},
    {"asme": "Symmetry", "gb": "对称度", "gb_standard": "GB/T 1182-2018", "note": "ASME 2018不推荐使用，建议用Position"},
    {"asme": "Circular Runout", "gb": "圆跳动", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Total Runout", "gb": "全跳动", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Profile of a Line", "gb": "线轮廓度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
    {"asme": "Profile of a Surface", "gb": "面轮廓度", "gb_standard": "GB/T 1182-2018", "note": "定义相同"},
]

# ASME Y14.5 修饰符
ASME_MODIFIERS = [
    {"symbol": "Ⓜ", "name": "最大实体要求 MMC", "name_en": "Maximum Material Condition",
     "description": "当特征尺寸偏离MMC时，允许公差增大。用于保证装配性。",
     "gb_equivalent": "GB/T 4249-2009 最大实体要求",
     "hover_explain": "最大实体要求(MMC)：当被测要素处于最大实体状态(MMC)时，几何公差为图样标注值。当实际尺寸偏离MMC时，几何公差可获得等于偏离量的补偿值。"},
    {"symbol": "Ⓛ", "name": "最小实体要求 LMC", "name_en": "Least Material Condition",
     "description": "当特征尺寸偏离LMC时，允许公差增大。用于保证最小壁厚。",
     "gb_equivalent": "GB/T 4249-2009 最小实体要求",
     "hover_explain": "最小实体要求(LMC)：当被测要素处于最小实体状态(LMC)时，几何公差为图样标注值。当实际尺寸偏离LMC时，几何公差可获得等于偏离量的补偿值。"},
    {"symbol": "Ⓔ", "name": "包容要求", "name_en": "Envelope Principle (Regardless of Feature Size)",
     "description": "要求特征表面不得超出最大实体边界。",
     "gb_equivalent": "GB/T 4249-2009 包容要求",
     "hover_explain": "包容要求：要求被测要素的实际表面不得超出最大实体边界(MMB)。即特征处处不得超出最大实体尺寸，且局部实际尺寸不得超出最小实体尺寸。"},
    {"symbol": "Ⓟ", "name": "延伸公差带", "name_en": "Projected Tolerance Zone",
     "description": "将公差带延伸到零件表面之外。",
     "gb_equivalent": "GB/T 1182-2018 延伸公差带",
     "hover_explain": "延伸公差带：将位置度等公差带延伸到零件装配表面之外一定距离，以控制零件装配后的配合精度。常用于螺栓、销钉的过孔。"},
    {"symbol": "Ⓡ", "name": "可逆要求", "name_en": "Reciprocity Requirement",
     "description": "允许尺寸公差和几何公差相互补偿。",
     "gb_equivalent": "GB/T 4249-2009 可逆要求",
     "hover_explain": "可逆要求：附加于最大实体要求或最小实体要求之上。当几何误差小于给定公差时，允许尺寸公差获得补偿，实现公差的动态分配。"},
    {"symbol": "Ⓕ", "name": "自由状态", "name_en": "Free State",
     "description": "适用于非刚性零件在自由状态下的公差要求。",
     "gb_equivalent": "GB/T 1182-2018 自由状态",
     "hover_explain": "自由状态条件：标注在公差框格后，表示该公差要求适用于零件在不受约束（自由状态）下的检测。常用于薄壁件、柔性件。"},
]
