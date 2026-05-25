# -*- coding: utf-8 -*-
"""
配合数据 (GB/T 1801-2009)
包含：常用配合数据库、配合推荐规则
"""

# --- 3.4 常用配合数据库 ---
COMMON_FITS_INFO = {
    # ---- 间隙配合 ----
    "H11/c11": {
        "designation": "H11/c11",
        "type": "间隙配合",
        "description": "大间隙配合，装配非常松，适用于高温、高速或受力变形较大的场合",
        "applications": [
            "农业机械中粗糙配合件",
            "高温工作的传动轴与轴承",
            "铁路车辆轴与轴承",
            "内燃机排气阀杆与导套"
        ],
        "assembly": "手轻松装配，无需任何工具"
    },
    "H9/d9": {
        "designation": "H9/d9",
        "type": "间隙配合",
        "description": "较大间隙配合，适用于转速较高、轴颈压力较大的场合",
        "applications": [
            "活塞与气缸套的配合",
            "滑块与导槽的配合",
            "空压机活塞与气缸",
            "离心泵叶轮与轴"
        ],
        "assembly": "手推装配，可用木锤轻击"
    },
    "H8/e8": {
        "designation": "H8/e8",
        "type": "间隙配合",
        "description": "中等间隙配合，适用于中等转速、中等载荷的转动配合",
        "applications": [
            "电机轴与轴承的配合",
            "主轴箱中中间轴与轴承",
            "自由齿轮与轴的配合",
            "减速器中齿轮与轴"
        ],
        "assembly": "手推装配"
    },
    "H8/f7": {
        "designation": "H8/f7",
        "type": "间隙配合",
        "description": "常用中等间隙配合，适用于一般转速的滑动轴承",
        "applications": [
            "机床主轴箱中齿轮与轴",
            "一般滑动轴承配合",
            "泵的柱塞与缸体",
            "变速箱中滑动齿轮"
        ],
        "assembly": "手推装配"
    },
    "H7/f6": {
        "designation": "H7/f6",
        "type": "间隙配合",
        "description": "精密间隙配合，间隙适中，广泛用于精密机械的转动配合",
        "applications": [
            "精密机床主轴与轴承",
            "分度头主轴与轴承",
            "精密齿轮与轴的配合",
            "液压系统中活塞与缸体"
        ],
        "assembly": "手推装配，配合精密"
    },
    "H7/g6": {
        "designation": "H7/g6",
        "type": "间隙配合",
        "description": "小间隙配合，间隙很小，用于精密定位和低速滑动",
        "applications": [
            "精密机床进给机构",
            "钻模衬套与钻头",
            "分度销与孔的配合",
            "精密仪表中的滑动配合"
        ],
        "assembly": "手轻推装配，配合精密"
    },
    "H7/h6": {
        "designation": "H7/h6",
        "type": "间隙配合",
        "description": "最小间隙为零的配合，用于精确定位和可拆卸连接",
        "applications": [
            "联轴器与轴的配合",
            "齿轮与轴的定位配合",
            "可换钻套与衬套",
            "手轮与轴的配合"
        ],
        "assembly": "手推或木锤装配"
    },
    "H8/h7": {
        "designation": "H8/h7",
        "type": "间隙配合",
        "description": "间隙接近零的配合，用于定位要求较高的可拆卸连接",
        "applications": [
            "皮带轮与轴的配合",
            "手柄与轴的配合",
            "一般定位销与孔",
            "凸轮与轴的配合"
        ],
        "assembly": "手推装配"
    },
    "H8/h8": {
        "designation": "H8/h8",
        "type": "间隙配合",
        "description": "零间隙配合，用于一般定位和可拆卸连接",
        "applications": [
            "法兰盘连接定位",
            "一般齿轮与轴",
            "减速器中齿轮与轴",
            "机床交换齿轮与轴"
        ],
        "assembly": "手推装配"
    },
    "H9/h9": {
        "designation": "H9/h9",
        "type": "间隙配合",
        "description": "零间隙配合，用于精度要求较低的定位",
        "applications": [
            "铰链连接",
            "粗定位销与孔",
            "一般法兰定位",
            "低精度齿轮与轴"
        ],
        "assembly": "手装配，有轻微间隙"
    },
    "G7/h6": {
        "designation": "G7/h6",
        "type": "间隙配合",
        "description": "基轴制小间隙配合，相当于H7/g6的基轴制形式",
        "applications": [
            "精密机床进给机构",
            "钻模衬套配合",
            "精密仪表滑动配合",
            "分度机构"
        ],
        "assembly": "手轻推装配"
    },
    "F8/h6": {
        "designation": "F8/h6",
        "type": "间隙配合",
        "description": "基轴制中等间隙配合，相当于H8/f7的基轴制形式",
        "applications": [
            "一般滑动轴承",
            "泵的活塞与缸体",
            "变速箱齿轮与轴",
            "电机轴与轴承"
        ],
        "assembly": "手推装配"
    },
    # ---- 过渡配合 ----
    "H7/js6": {
        "designation": "H7/js6",
        "type": "过渡配合",
        "description": "过盈概率很小的过渡配合，拆卸方便，定位精度高",
        "applications": [
            "联轴器与轴",
            "齿轮与轴（需拆卸）",
            "手轮与轴",
            "精密定位件"
        ],
        "assembly": "手锤或木锤轻轻装配"
    },
    "H7/k6": {
        "designation": "H7/k6",
        "type": "过渡配合",
        "description": "最常用的过渡配合，过盈概率适中，装卸方便",
        "applications": [
            "减速器齿轮与轴",
            "皮带轮与轴",
            "联轴器与轴",
            "滚动轴承外圈与座孔"
        ],
        "assembly": "手锤轻轻打入"
    },
    "H7/m6": {
        "designation": "H7/m6",
        "type": "过渡配合",
        "description": "过盈概率较大的过渡配合，定位可靠，拆卸较困难",
        "applications": [
            "蜗轮与轴",
            "凸轮与轴",
            "齿轮与轴（不常拆卸）",
            "联轴器与轴"
        ],
        "assembly": "铜锤或压力机装配"
    },
    "H7/n6": {
        "designation": "H7/n6",
        "type": "过渡配合",
        "description": "接近过盈配合的过渡配合，几乎不拆卸",
        "applications": [
            "振动机械的齿轮与轴",
            "重型机械定位件",
            "不常拆卸的联轴器",
            "高精度定位销"
        ],
        "assembly": "压力机装配"
    },
    "JS7/h6": {
        "designation": "JS7/h6",
        "type": "过渡配合",
        "description": "基轴制过渡配合，过盈概率很小，拆卸方便",
        "applications": [
            "可拆卸齿轮与轴",
            "手轮与轴",
            "联轴器与轴",
            "定位套与轴"
        ],
        "assembly": "手锤轻轻装配"
    },
    "K7/h6": {
        "designation": "K7/h6",
        "type": "过渡配合",
        "description": "基轴制过渡配合，最常用的过渡配合形式",
        "applications": [
            "皮带轮与轴",
            "齿轮与轴",
            "联轴器与轴",
            "滚动轴承内圈与轴"
        ],
        "assembly": "手锤轻轻打入"
    },
    "N7/h6": {
        "designation": "N7/h6",
        "type": "过渡配合",
        "description": "基轴制过渡配合，接近过盈配合",
        "applications": [
            "不常拆卸的齿轮与轴",
            "重型机械定位件",
            "振动件的连接",
            "高精度定位"
        ],
        "assembly": "压力机装配"
    },
    # ---- 过盈配合 ----
    "H7/p6": {
        "designation": "H7/p6",
        "type": "过盈配合",
        "description": "轻型过盈配合，用于不常拆卸的固定连接",
        "applications": [
            "轴承衬套与座孔",
            "齿轮与轴（不拆卸）",
            "蜗轮轮缘与轮芯",
            "定位销与孔"
        ],
        "assembly": "压力机压入"
    },
    "H7/r6": {
        "designation": "H7/r6",
        "type": "过盈配合",
        "description": "中型过盈配合，传递中等载荷",
        "applications": [
            "蜗轮轮缘与轮芯的装配",
            "连杆小头衬套与孔",
            "固定齿轮与轴",
            "曲柄销与曲柄"
        ],
        "assembly": "压力机或热胀法装配"
    },
    "H7/s6": {
        "designation": "H7/s6",
        "type": "过盈配合",
        "description": "重型过盈配合，传递较大载荷，永久性装配",
        "applications": [
            "火车车轮与轴",
            "曲轴与飞轮",
            "大型电机转子与轴",
            "永久性连接的齿轮"
        ],
        "assembly": "热胀法或油压法装配"
    },
    "H7/u6": {
        "designation": "H7/u6",
        "type": "过盈配合",
        "description": "特重型过盈配合，传递重载荷，永久性装配",
        "applications": [
            "重型机械的永久连接",
            "大型齿轮与轴",
            "柴油机喷油泵柱塞套",
            "高压容器端盖"
        ],
        "assembly": "热胀法装配（加热孔件）"
    },
    "P7/h6": {
        "designation": "P7/h6",
        "type": "过盈配合",
        "description": "基轴制轻型过盈配合",
        "applications": [
            "轴承衬套与座孔",
            "不拆卸的定位件",
            "齿轮与轴的固定连接",
            "衬套与壳体"
        ],
        "assembly": "压力机压入"
    },
}

# --- 3.5 配合推荐规则 ---
FIT_RECOMMENDATION_RULES = [
    {
        "conditions": {
            "load": "轻载",
            "speed": "低速",
            "precision": "一般",
            "disassembly": "频繁拆卸"
        },
        "fits": ["H7/h6", "H8/h7", "H9/h9"],
        "reason": "轻载低速且需频繁拆卸，选用间隙接近零的配合（H/h），保证定位精度同时便于装拆"
    },
    {
        "conditions": {
            "load": "轻载",
            "speed": "中速",
            "precision": "较高",
            "disassembly": "偶尔拆卸"
        },
        "fits": ["H7/g6", "H7/f6"],
        "reason": "轻载中速且精度要求较高，选用小间隙配合（H/g、H/f），保证运转平稳"
    },
    {
        "conditions": {
            "load": "中载",
            "speed": "中速",
            "precision": "一般",
            "disassembly": "偶尔拆卸"
        },
        "fits": ["H7/k6", "H7/js6"],
        "reason": "中载中速且偶尔拆卸，选用过渡配合（H/k、H/js），兼顾定位精度和可拆卸性"
    },
    {
        "conditions": {
            "load": "中载",
            "speed": "中速",
            "precision": "较高",
            "disassembly": "不拆卸"
        },
        "fits": ["H7/n6", "H7/m6"],
        "reason": "中载中速且不拆卸，选用过盈概率较大的过渡配合（H/n、H/m），保证连接可靠"
    },
    {
        "conditions": {
            "load": "重载",
            "speed": "低速",
            "precision": "一般",
            "disassembly": "不拆卸"
        },
        "fits": ["H7/p6", "H7/r6"],
        "reason": "重载低速且不拆卸，选用轻型到中型过盈配合（H/p、H/r），依靠过盈传递载荷"
    },
    {
        "conditions": {
            "load": "重载",
            "speed": "低速",
            "precision": "一般",
            "disassembly": "永久装配"
        },
        "fits": ["H7/s6", "H7/u6"],
        "reason": "重载低速且永久装配，选用重型过盈配合（H/s、H/u），确保连接牢固可靠"
    },
    {
        "conditions": {
            "load": "轻载",
            "speed": "高速",
            "precision": "高精度",
            "disassembly": "偶尔拆卸"
        },
        "fits": ["H7/g6", "H6/g5"],
        "reason": "高速轻载高精度，选用小间隙精密配合（H/g），保证高速运转的润滑和精度"
    },
    {
        "conditions": {
            "load": "中载",
            "speed": "高速",
            "precision": "较高",
            "disassembly": "偶尔拆卸"
        },
        "fits": ["H8/f7", "H7/f6"],
        "reason": "中载高速，选用中等间隙配合（H/f），保证良好的润滑条件和运转灵活性"
    },
    {
        "conditions": {
            "load": "轻载",
            "speed": "低速",
            "precision": "一般",
            "disassembly": "自由装配"
        },
        "fits": ["H7/h6", "H9/h9"],
        "reason": "仅需定位且自由装配，选用零间隙配合（H/h），装拆方便，定位准确"
    },
    {
        "conditions": {
            "load": "重载",
            "speed": "中速",
            "precision": "一般",
            "disassembly": "不拆卸"
        },
        "fits": ["H7/r6", "H7/s6"],
        "reason": "重载中速不拆卸，选用中型到重型过盈配合，确保连接强度"
    },
    {
        "conditions": {
            "load": "轻载",
            "speed": "中速",
            "precision": "一般",
            "disassembly": "自由装配"
        },
        "fits": ["H8/e8", "H9/d9"],
        "reason": "轻载中速自由装配，选用较大间隙配合（H/e、H/d），装配方便"
    },
    {
        "conditions": {
            "load": "中载",
            "speed": "低速",
            "precision": "较高",
            "disassembly": "不拆卸"
        },
        "fits": ["H7/m6", "H7/n6"],
        "reason": "中载低速高精度不拆卸，选用过渡配合偏向过盈，保证定位精度和连接可靠性"
    },
    {
        "conditions": {
            "load": "轻载",
            "speed": "高速",
            "precision": "高精度",
            "disassembly": "不拆卸"
        },
        "fits": ["H6/g5", "H6/f5"],
        "reason": "高速轻载高精度不拆卸，选用高精度小间隙配合，保证高速运转精度"
    },
    {
        "conditions": {
            "load": "重载",
            "speed": "高速",
            "precision": "一般",
            "disassembly": "永久装配"
        },
        "fits": ["H7/u6", "H7/s6"],
        "reason": "重载高速永久装配，选用重型过盈配合，确保在高速重载下连接不松动"
    },
    {
        "conditions": {
            "load": "中载",
            "speed": "低速",
            "precision": "一般",
            "disassembly": "偶尔拆卸"
        },
        "fits": ["H7/k6", "H7/js6"],
        "reason": "中载低速偶尔拆卸，选用过渡配合，兼顾定位精度和可拆卸性"
    },
    {
        "conditions": {
            "load": "轻载",
            "speed": "低速",
            "precision": "低精度",
            "disassembly": "自由装配"
        },
        "fits": ["H11/c11", "H9/d9"],
        "reason": "低精度自由装配，选用大间隙配合，降低加工成本"
    },
    {
        "conditions": {
            "load": "重载",
            "speed": "低速",
            "precision": "较高",
            "disassembly": "永久装配"
        },
        "fits": ["H7/s6", "H7/u6"],
        "reason": "重载低速高精度永久装配，选用重型过盈配合，保证连接强度和精度"
    },
]
