# 公差等级-成本关联数据
TOLERANCE_COST_DATA = {
    "IT5": {"cost_index": 100, "relative_cost": "基准", "cost_increase": "—", "typical_process": "精磨、研磨、珩磨"},
    "IT6": {"cost_index": 60, "relative_cost": "约为IT5的60%", "cost_increase": "IT5比IT6成本增加约67%", "typical_process": "精磨、精车、精镗"},
    "IT7": {"cost_index": 40, "relative_cost": "约为IT5的40%", "cost_increase": "IT6比IT7成本增加约50%", "typical_process": "精车、精铣、磨削"},
    "IT8": {"cost_index": 25, "relative_cost": "约为IT5的25%", "cost_increase": "IT7比IT8成本增加约60%", "typical_process": "普通车削、铣削、镗削"},
    "IT9": {"cost_index": 16, "relative_cost": "约为IT5的16%", "cost_increase": "IT8比IT9成本增加约56%", "typical_process": "普通车削、铣削、钻削"},
    "IT10": {"cost_index": 10, "relative_cost": "约为IT5的10%", "cost_increase": "IT9比IT10成本增加约60%", "typical_process": "粗车、粗铣、钻削"},
    "IT11": {"cost_index": 7, "relative_cost": "约为IT5的7%", "cost_increase": "IT10比IT11成本增加约43%", "typical_process": "粗加工、锯割"},
    "IT12": {"cost_index": 5, "relative_cost": "约为IT5的5%", "cost_increase": "IT11比IT12成本增加约40%", "typical_process": "粗加工、冲裁"},
}

# 加工工艺经济精度范围
PROCESS_PRECISION = [
    {"process": "研磨", "precision_range": "IT01~IT5", "surface_roughness": "Ra 0.012~0.1", "cost_level": "很高"},
    {"process": "珩磨", "precision_range": "IT4~IT7", "surface_roughness": "Ra 0.025~0.2", "cost_level": "很高"},
    {"process": "精磨", "precision_range": "IT5~IT7", "surface_roughness": "Ra 0.1~0.4", "cost_level": "高"},
    {"process": "精车", "precision_range": "IT6~IT8", "surface_roughness": "Ra 0.4~1.6", "cost_level": "中等"},
    {"process": "精铣", "precision_range": "IT6~IT8", "surface_roughness": "Ra 0.4~1.6", "cost_level": "中等"},
    {"process": "精镗", "precision_range": "IT6~IT8", "surface_roughness": "Ra 0.4~1.6", "cost_level": "中等"},
    {"process": "普通车削", "precision_range": "IT8~IT11", "surface_roughness": "Ra 1.6~6.3", "cost_level": "低"},
    {"process": "普通铣削", "precision_range": "IT8~IT11", "surface_roughness": "Ra 1.6~6.3", "cost_level": "低"},
    {"process": "钻削", "precision_range": "IT10~IT13", "surface_roughness": "Ra 3.2~12.5", "cost_level": "低"},
    {"process": "粗车", "precision_range": "IT10~IT12", "surface_roughness": "Ra 6.3~25", "cost_level": "很低"},
    {"process": "粗铣", "precision_range": "IT10~IT12", "surface_roughness": "Ra 6.3~25", "cost_level": "很低"},
    {"process": "锯割", "precision_range": "IT12~IT15", "surface_roughness": "Ra 25~100", "cost_level": "很低"},
    {"process": "冲裁", "precision_range": "IT10~IT14", "surface_roughness": "Ra 1.6~12.5", "cost_level": "低"},
    {"process": "铸造", "precision_range": "IT14~IT18", "surface_roughness": "Ra 12.5~100", "cost_level": "很低"},
    {"process": "锻造", "precision_range": "IT14~IT18", "surface_roughness": "Ra 12.5~100", "cost_level": "很低"},
    {"process": "挤压", "precision_range": "IT8~IT11", "surface_roughness": "Ra 0.4~3.2", "cost_level": "中等"},
    {"process": "电火花", "precision_range": "IT6~IT9", "surface_roughness": "Ra 0.8~6.3", "cost_level": "高"},
    {"process": "线切割", "precision_range": "IT6~IT8", "surface_roughness": "Ra 0.4~3.2", "cost_level": "高"},
]

# 常用材料热膨胀系数 (×10⁻⁶/°C)
THERMAL_EXPANSION_DATA = [
    {"material": "铝合金(Al)", "coefficient": 23.1, "range": "20~100°C", "note": "热膨胀系数最大，精密配合需特别注意"},
    {"material": "铜合金(Cu)", "coefficient": 17.5, "range": "20~100°C", "note": "常用于导电/导热零件"},
    {"material": "黄铜(H62)", "coefficient": 20.6, "range": "20~100°C", "note": "铜锌合金"},
    {"material": "碳钢(45#)", "coefficient": 11.5, "range": "20~100°C", "note": "最常用的结构钢"},
    {"material": "合金钢(40Cr)", "coefficient": 11.0, "range": "20~100°C", "note": "常用调质钢"},
    {"material": "不锈钢(304)", "coefficient": 17.3, "range": "20~100°C", "note": "奥氏体不锈钢"},
    {"material": "铸铁(HT200)", "coefficient": 10.5, "range": "20~100°C", "note": "常用铸铁"},
    {"material": "钛合金(TC4)", "coefficient": 8.6, "range": "20~100°C", "note": "航空航天常用"},
    {"material": "铸铝(ZL104)", "coefficient": 21.4, "range": "20~100°C", "note": "铸造铝合金"},
    {"material": "工具钢(T8A)", "coefficient": 11.0, "range": "20~100°C", "note": "碳素工具钢"},
    {"material": "镍合金", "coefficient": 13.3, "range": "20~100°C", "note": "耐高温合金"},
    {"material": "工程塑料(PA66)", "coefficient": 80.0, "range": "20~60°C", "note": "尼龙，热膨胀极大"},
    {"material": "玻璃", "coefficient": 9.0, "range": "20~100°C", "note": "硼硅玻璃"},
    {"material": "陶瓷(Al₂O₃)", "coefficient": 7.0, "range": "20~500°C", "note": "氧化铝陶瓷"},
]

# 表面粗糙度关联推荐
SURFACE_ROUGHNESS_DATA = [
    {"ra_value": 0.1, "grade": "N1", "process": "镜面磨削、抛光", "application": "量规工作面、精密轴承滚道", "cost_note": "成本极高，仅用于精密量具"},
    {"ra_value": 0.2, "grade": "N2", "process": "精磨、研磨", "application": "液压阀芯、精密轴颈", "cost_note": "成本很高"},
    {"ra_value": 0.4, "grade": "N3", "process": "精磨、珩磨", "application": "活塞销、曲轴轴颈", "cost_note": "成本高"},
    {"ra_value": 0.8, "grade": "N4", "process": "精磨、精车", "application": "轴承配合面、齿轮齿面", "cost_note": "成本较高，精密配合常用"},
    {"ra_value": 1.6, "grade": "N5", "process": "精车、精铣、磨削", "application": "普通轴颈、销孔", "cost_note": "成本中等，最常用的精密表面"},
    {"ra_value": 3.2, "grade": "N6", "process": "普通车削、铣削", "application": "一般配合面、安装面", "cost_note": "成本较低，通用机械常用"},
    {"ra_value": 6.3, "grade": "N7", "process": "粗车、粗铣", "application": "非配合面、支架底面", "cost_note": "成本低"},
    {"ra_value": 12.5, "grade": "N8", "process": "粗加工、锯割", "application": "非重要表面", "cost_note": "成本很低"},
    {"ra_value": 25.0, "grade": "N9", "process": "粗加工", "application": "毛坯面、自由面", "cost_note": "成本极低"},
]

# ISO 2768 通用公差标准
ISO_2768_DATA = {
    "permissible_variations": {
        "fine": "f",
        "medium": "m",
        "coarse": "c",
        "very_coarse": "v",
    },
    "tolerance_classes": {
        "linear": {
            "description": "线性尺寸的未注公差",
            "fine": [0.05, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5],
            "medium": [0.1, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2],
            "coarse": [0.2, 0.3, 0.5, 0.8, 1.2, 2.0, 3.0],
            "very_coarse": [0.5, 1.0, 1.5, 2.5, 4.0, 6.0, 8.0],
            "ranges": ["0.5~3", "3~6", "6~30", "30~120", "120~400", "400~1000", "1000~2000"],
        },
        "angular": {
            "description": "角度尺寸的未注公差",
            "classes": ["精密级f", "中等级m", "粗糙级c", "最粗级v"],
        },
    },
    "gb_equivalent": "GB/T 1804-2000 一般公差 未注公差的线性和角度尺寸的公差",
}

# 工况智能推荐数据
WORKING_CONDITION_RECOMMENDATIONS = [
    {
        "condition": "旋转精度要求高",
        "keywords": ["旋转", "精度", "高速", "精密", "主轴"],
        "recommended_fits": [
            {"fit": "H6/g5", "type": "间隙配合", "reason": "高精度滑动配合，间隙极小，保证旋转精度。用于精密主轴轴承配合。", "assembly": "需精密装配"},
            {"fit": "H6/h5", "type": "间隙配合", "reason": "零间隙配合，可手动推入。用于分度头主轴等精密定位。", "assembly": "手推装配"},
            {"fit": "H5/js4", "type": "过渡配合", "reason": "极精密过渡配合，几乎无间隙。用于超精密主轴。", "assembly": "轻压装配"},
        ],
        "geo_tolerance": "圆度5~6级，圆柱度5~6级，同轴度5级，径向圆跳动5级",
        "roughness": "Ra 0.4~0.8",
    },
    {
        "condition": "承受较大载荷",
        "keywords": ["载荷", "承载", "重载", "扭矩", "传力"],
        "recommended_fits": [
            {"fit": "H7/p6", "type": "过盈配合", "reason": "轻过盈配合，可传递中等扭矩。装配需压力机。", "assembly": "压力机压入"},
            {"fit": "H7/r6", "type": "过盈配合", "reason": "中等过盈配合，可传递较大扭矩，可少量用键辅助。", "assembly": "压力机压入"},
            {"fit": "H7/s6", "type": "过盈配合", "reason": "重过盈配合，可传递大扭矩。需加热或冷却装配。", "assembly": "热装或冷缩装配"},
            {"fit": "H7/u6", "type": "过盈配合", "reason": "极重过盈配合，可传递极大扭矩。永久性连接。", "assembly": "热装"},
        ],
        "geo_tolerance": "圆度6~7级，圆柱度6~7级，同轴度6级",
        "roughness": "Ra 0.8~1.6",
    },
    {
        "condition": "需要经常拆卸",
        "keywords": ["拆卸", "维修", "更换", "可拆", "维护"],
        "recommended_fits": [
            {"fit": "H7/js6", "type": "过渡配合", "reason": "易拆卸过渡配合，用手锤轻击即可装卸。用于需要经常维护的场合。", "assembly": "手锤轻击"},
            {"fit": "H7/k6", "type": "过渡配合", "reason": "标准过渡配合，用手锤装卸。是最常用的过渡配合。", "assembly": "手锤装卸"},
            {"fit": "H7/h6", "type": "间隙配合", "reason": "零间隙配合，可自由拆卸。用于定位要求高但需经常拆卸的场合。", "assembly": "手推装配"},
        ],
        "geo_tolerance": "圆度7~8级，同轴度7级",
        "roughness": "Ra 1.6~3.2",
    },
    {
        "condition": "滑动运动",
        "keywords": ["滑动", "导轨", "滑块", "往复", "移动"],
        "recommended_fits": [
            {"fit": "H7/f6", "type": "间隙配合", "reason": "常用滑动配合，间隙适中，润滑良好。用于一般滑动导轨。", "assembly": "手推装配"},
            {"fit": "H7/g6", "type": "间隙配合", "reason": "精密滑动配合，间隙小。用于精密导轨和定位滑动。", "assembly": "手推装配"},
            {"fit": "H8/f7", "type": "间隙配合", "reason": "宽松滑动配合，间隙较大。用于一般精度要求的滑动面。", "assembly": "手推装配"},
            {"fit": "H9/d9", "type": "间隙配合", "reason": "宽松转动配合，间隙大。用于低速滑动和不重要场合。", "assembly": "手推装配"},
        ],
        "geo_tolerance": "直线度6~8级，平面度6~8级，平行度6~8级",
        "roughness": "Ra 0.8~1.6",
    },
    {
        "condition": "高速旋转",
        "keywords": ["高速", "转速", "电机", "涡轮", "离心"],
        "recommended_fits": [
            {"fit": "H6/g5", "type": "间隙配合", "reason": "高速精密滑动配合，间隙小且均匀，保证油膜形成。", "assembly": "精密装配"},
            {"fit": "H6/h5", "type": "间隙配合", "reason": "高速零间隙配合。用于高速主轴和精密轴承。", "assembly": "精密装配"},
            {"fit": "H7/js5", "type": "过渡配合", "reason": "高速过渡配合，平衡精度与承载。用于高速齿轮与轴。", "assembly": "轻压装配"},
        ],
        "geo_tolerance": "圆度5~6级，圆柱度5~6级，动平衡要求高",
        "roughness": "Ra 0.2~0.4",
    },
    {
        "condition": "密封要求",
        "keywords": ["密封", "防漏", "液压", "气动", "油缸"],
        "recommended_fits": [
            {"fit": "H7/h6", "type": "间隙配合", "reason": "零间隙配合，用于O形圈密封沟槽。密封性好且可拆卸。", "assembly": "手推装配"},
            {"fit": "H8/f7", "type": "间隙配合", "reason": "小间隙配合，用于活塞与缸体的滑动密封。", "assembly": "手推装配"},
            {"fit": "H7/g6", "type": "间隙配合", "reason": "精密小间隙配合，用于液压阀芯与阀体。", "assembly": "手推装配"},
        ],
        "geo_tolerance": "圆柱度6~7级，圆度6~7级，直线度6~8级",
        "roughness": "Ra 0.4~0.8",
    },
    {
        "condition": "精密定位",
        "keywords": ["定位", "对中", "分度", "夹具", "模具"],
        "recommended_fits": [
            {"fit": "H7/h6", "type": "间隙配合", "reason": "零间隙配合，定位精度高。用于夹具定位销、模具导柱。", "assembly": "手推装配"},
            {"fit": "H7/js6", "type": "过渡配合", "reason": "精密过渡配合，几乎无间隙。用于精密分度定位。", "assembly": "手锤轻击"},
            {"fit": "H7/k6", "type": "过渡配合", "reason": "标准过渡配合，定位可靠。用于一般定位销。", "assembly": "手锤装卸"},
        ],
        "geo_tolerance": "位置度6~8级，同轴度6~8级，对称度7~9级",
        "roughness": "Ra 0.8~1.6",
    },
    {
        "condition": "高温工况",
        "keywords": ["高温", "热", "温度", "膨胀", "发动机"],
        "recommended_fits": [
            {"fit": "H8/e7", "type": "间隙配合", "reason": "较大间隙配合，预留热膨胀空间。用于高温工况的滑动配合。", "assembly": "手推装配"},
            {"fit": "H9/d9", "type": "间隙配合", "reason": "大间隙配合，补偿热膨胀。用于发动机活塞与缸套。", "assembly": "手推装配"},
        ],
        "geo_tolerance": "注意热膨胀对公差的影响，建议预留热膨胀间隙",
        "roughness": "Ra 1.6~3.2",
        "note": "高温工况需考虑材料热膨胀系数差异，使用ΔL=α·L·ΔT计算预留间隙",
    },
]
