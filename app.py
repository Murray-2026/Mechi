# -*- coding: utf-8 -*-
"""
机械公差助手 - 基于 GB/T 1800.1-2020 和 GB/T 1184-1996 标准
功能：公差查询、配合查询、配合推荐、形位公差查询、尺寸链计算
"""

# ============================================================
# 第1节：导入库和页面配置
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import math
import re
import copy

st.set_page_config(page_title="机械公差助手", page_icon="⚙️", layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# 第2节：自定义CSS样式
# ============================================================


# ============================================================
# 第3节：标准公差数据表 (GB/T 1800.1-2020)
# ============================================================

# --- 3.1 尺寸分段 (mm) ---
SIZE_RANGES = [
    (0, 3), (3, 6), (6, 10), (10, 18), (18, 30),
    (30, 50), (50, 80), (80, 120), (120, 180),
    (180, 250), (250, 315), (315, 400), (400, 500)
]

# --- 3.2 IT01-IT18 标准公差值 (微米) ---
# 每个等级对应13个尺寸段的公差值
IT_VALUES = {
    "IT01": [0.3, 0.4, 0.4, 0.5, 0.6, 0.6, 0.8, 1.0, 1.2, 2.0, 2.5, 3.0, 4.0],
    "IT0":  [0.5, 0.6, 0.6, 0.8, 1.0, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0],
    "IT1":  [0.8, 1.0, 1.0, 1.2, 1.5, 1.5, 2.0, 2.5, 3.5, 4.5, 6.0, 7.0, 8.0],
    "IT2":  [1.2, 1.5, 1.5, 2.0, 2.5, 2.5, 3.0, 4.0, 5.0, 7.0, 8.0, 9.0, 10.0],
    "IT3":  [2.0, 2.5, 2.5, 3.0, 4.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 13.0, 16.0],
    "IT4":  [3, 4, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20],
    "IT5":  [4, 5, 6, 8, 9, 11, 13, 16, 18, 20, 23, 25, 27],
    "IT6":  [6, 8, 9, 11, 13, 16, 19, 22, 25, 29, 32, 36, 40],
    "IT7":  [10, 12, 15, 18, 21, 25, 30, 35, 40, 46, 52, 57, 63],
    "IT8":  [14, 18, 22, 27, 33, 39, 46, 54, 63, 72, 81, 89, 97],
    "IT9":  [25, 30, 36, 43, 52, 62, 74, 87, 100, 115, 130, 140, 155],
    "IT10": [40, 48, 58, 70, 84, 100, 120, 140, 160, 185, 210, 230, 250],
    "IT11": [60, 75, 90, 110, 130, 160, 190, 220, 250, 290, 320, 360, 400],
    "IT12": [100, 120, 150, 180, 210, 250, 300, 350, 400, 460, 520, 570, 630],
    "IT13": [140, 180, 220, 270, 330, 390, 460, 540, 630, 720, 810, 890, 970],
    "IT14": [250, 300, 360, 430, 520, 620, 740, 870, 1000, 1150, 1300, 1400, 1550],
    "IT15": [400, 480, 580, 700, 840, 1000, 1200, 1400, 1600, 1850, 2100, 2300, 2500],
    "IT16": [600, 750, 900, 1100, 1300, 1600, 1900, 2200, 2500, 2900, 3200, 3600, 4000],
    "IT17": [1000, 1200, 1500, 1800, 2100, 2500, 3000, 3500, 4000, 4600, 5200, 5700, 6300],
    "IT18": [1400, 1800, 2200, 2700, 3300, 3900, 4600, 5400, 6300, 7200, 8100, 8900, 9700],
}

# --- 3.3 形位公差数据表 (GB/T 1184-1996) ---

# 圆度/圆柱度 - 13个直径范围, 等级0-12
CIRCULARITY_DIAMETER_RANGES = [
    (0, 3), (3, 6), (6, 10), (10, 18), (18, 30),
    (30, 50), (50, 80), (80, 120), (120, 180),
    (180, 250), (250, 315), (315, 400), (400, 500)
]

CIRCULARITY_VALUES = {
    0:  [0.1, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5],
    1:  [0.2, 0.2, 0.25, 0.25, 0.3, 0.4, 0.5, 0.6, 1.0, 1.2, 1.6, 2.0, 2.5],
    2:  [0.3, 0.4, 0.4, 0.5, 0.6, 0.6, 0.8, 1.0, 1.2, 2.0, 2.5, 3.0, 4.0],
    3:  [0.5, 0.6, 0.6, 0.8, 1.0, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0],
    4:  [0.8, 1.0, 1.0, 1.2, 1.5, 1.5, 2.0, 2.5, 3.5, 4.5, 6.0, 7.0, 8.0],
    5:  [1.2, 1.5, 1.5, 2.0, 2.5, 2.5, 3.0, 4.0, 5.0, 7.0, 8.0, 9.0, 10.0],
    6:  [2.0, 2.5, 2.5, 3.0, 4.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 13.0, 15.0],
    7:  [3.0, 4.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0],
    8:  [4.0, 5.0, 6.0, 8.0, 9.0, 11.0, 13.0, 15.0, 18.0, 20.0, 23.0, 25.0, 27.0],
    9:  [6.0, 8.0, 9.0, 11.0, 13.0, 16.0, 19.0, 22.0, 25.0, 29.0, 32.0, 36.0, 40.0],
    10: [10.0, 12.0, 15.0, 18.0, 21.0, 25.0, 30.0, 35.0, 40.0, 46.0, 52.0, 57.0, 63.0],
    11: [14.0, 18.0, 22.0, 27.0, 33.0, 39.0, 46.0, 54.0, 63.0, 72.0, 81.0, 89.0, 97.0],
    12: [25.0, 30.0, 36.0, 43.0, 52.0, 62.0, 74.0, 87.0, 100.0, 115.0, 130.0, 140.0, 155.0],
}

# 直线度/平面度 - 10个长度范围, 等级1-12
STRAIGHTNESS_LENGTH_RANGES = [
    (0, 10), (10, 16), (16, 25), (25, 40), (40, 63),
    (63, 100), (100, 160), (160, 250), (250, 400), (400, 630)
]

STRAIGHTNESS_VALUES = {
    1:  [0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5],
    2:  [0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0],
    3:  [0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0],
    4:  [1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
    5:  [2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0],
    6:  [3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0],
    7:  [5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0],
    8:  [8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0],
    9:  [12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0],
    10: [20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0],
    11: [30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0],
    12: [60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0],
}

# 平行度/垂直度 - 10个长度范围, 等级1-12
PARALLELISM_LENGTH_RANGES = [
    (0, 10), (10, 16), (16, 25), (25, 40), (40, 63),
    (63, 100), (100, 160), (160, 250), (250, 400), (400, 630)
]

PARALLELISM_VALUES = {
    1:  [0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0],
    2:  [0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0],
    3:  [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0],
    4:  [3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0],
    5:  [5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0],
    6:  [8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0],
    7:  [12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0],
    8:  [20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0],
    9:  [30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0],
    10: [50.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0, 300.0, 400.0],
    11: [80.0, 100.0, 120.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0, 600.0],
    12: [120.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0, 600.0, 800.0, 1000.0],
}

# 同轴度/对称度/圆跳动 - 10个直径范围, 等级1-12
COAXIALITY_DIAMETER_RANGES = [
    (0, 1), (1, 3), (3, 6), (6, 10), (10, 18),
    (18, 30), (30, 50), (50, 120), (120, 250), (250, 500)
]

COAXIALITY_VALUES = {
    1:  [0.4, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5],
    2:  [0.6, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0],
    3:  [1.0, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0],
    4:  [1.5, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
    5:  [2.5, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0],
    6:  [4.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0],
    7:  [6.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0],
    8:  [10.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0],
    9:  [15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0],
    10: [25.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0],
    11: [40.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0, 300.0, 400.0],
    12: [60.0, 120.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0, 600.0, 800.0],
}

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

# --- 3.6 形位公差推荐 ---
GEOMETRIC_TOLERANCE_RECOMMENDATIONS = {
    "轴": {
        "支撑轴颈": [
            {
                "item": "圆度",
                "grade_range": (5, 7),
                "reason": "支撑轴颈圆度直接影响轴承运转精度，一般选用5-7级"
            },
            {
                "item": "圆柱度",
                "grade_range": (5, 7),
                "reason": "圆柱度影响轴承配合质量，与圆度等级协调"
            },
            {
                "item": "同轴度",
                "grade_range": (5, 8),
                "reason": "多轴颈同轴度影响装配精度和运转平稳性"
            },
            {
                "item": "圆跳动",
                "grade_range": (6, 8),
                "reason": "综合反映轴颈形状和位置误差"
            },
        ],
        "安装齿轮段": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "齿轮安装段圆度影响齿轮啮合精度"
            },
            {
                "item": "同轴度（相对基准轴颈）",
                "grade_range": (6, 8),
                "reason": "齿轮段与支撑轴颈的同轴度影响齿轮啮合质量"
            },
            {
                "item": "端面跳动",
                "grade_range": (6, 8),
                "reason": "齿轮定位端面的跳动影响齿轮轴向定位精度"
            },
        ],
        "键槽": [
            {
                "item": "对称度",
                "grade_range": (7, 9),
                "reason": "键槽对称度影响键的装配质量和受力均匀性"
            },
        ],
    },
    "孔": {
        "轴承孔": [
            {
                "item": "圆度",
                "grade_range": (5, 7),
                "reason": "轴承孔圆度直接影响轴承外圈配合质量"
            },
            {
                "item": "圆柱度",
                "grade_range": (5, 7),
                "reason": "圆柱度影响轴承配合的均匀性"
            },
            {
                "item": "同轴度（多孔）",
                "grade_range": (6, 8),
                "reason": "多轴承孔同轴度影响轴的装配和运转精度"
            },
        ],
        "定位销孔": [
            {
                "item": "位置度",
                "grade_range": (7, 9),
                "reason": "定位销孔位置度直接影响定位精度"
            },
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "销孔圆度影响销的配合质量"
            },
        ],
        "螺纹孔": [
            {
                "item": "位置度",
                "grade_range": (8, 10),
                "reason": "螺纹孔位置度影响螺栓的装配"
            },
            {
                "item": "垂直度（相对端面）",
                "grade_range": (8, 10),
                "reason": "螺纹孔垂直度影响螺栓拧入质量"
            },
        ],
    },
    "箱体": {
        "轴承孔系": [
            {
                "item": "平行度（孔系间）",
                "grade_range": (5, 7),
                "reason": "轴承孔系平行度直接影响齿轮啮合精度"
            },
            {
                "item": "同轴度（同轴孔）",
                "grade_range": (6, 8),
                "reason": "同轴孔的同轴度影响轴的装配精度"
            },
            {
                "item": "位置度",
                "grade_range": (6, 8),
                "reason": "孔系位置度影响齿轮中心距精度"
            },
            {
                "item": "平面度（结合面）",
                "grade_range": (6, 8),
                "reason": "箱体结合面平面度影响密封性能"
            },
        ],
        "安装面": [
            {
                "item": "平面度",
                "grade_range": (6, 9),
                "reason": "安装面平面度影响部件安装精度"
            },
            {
                "item": "平行度（相对基准面）",
                "grade_range": (6, 9),
                "reason": "安装面平行度影响安装后部件的位置精度"
            },
        ],
    },
    "法兰": {
        "密封面": [
            {
                "item": "平面度",
                "grade_range": (5, 8),
                "reason": "法兰密封面平面度直接影响密封性能"
            },
            {
                "item": "平行度（相对结合面）",
                "grade_range": (6, 8),
                "reason": "法兰面平行度影响螺栓预紧力的均匀性"
            },
        ],
        "螺栓孔": [
            {
                "item": "位置度",
                "grade_range": (8, 10),
                "reason": "螺栓孔位置度影响螺栓装配"
            },
        ],
        "定位止口": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "定位止口圆度影响法兰定位精度"
            },
            {
                "item": "同轴度（相对密封面）",
                "grade_range": (6, 8),
                "reason": "止口与密封面的同轴度影响密封效果"
            },
        ],
    },
    "端盖": {
        "定位面": [
            {
                "item": "平面度",
                "grade_range": (6, 8),
                "reason": "端盖定位面平面度影响密封和安装精度"
            },
            {
                "item": "垂直度（相对轴线）",
                "grade_range": (6, 8),
                "reason": "端面与轴线的垂直度影响密封效果"
            },
        ],
        "轴承孔（如有）": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "端盖轴承孔圆度影响轴承配合质量"
            },
            {
                "item": "同轴度",
                "grade_range": (7, 9),
                "reason": "端盖孔与箱体孔的同轴度影响轴的装配"
            },
        ],
    },
}

# ============================================================
# 第4节：核心计算函数
# ============================================================

# --- 4.1 辅助函数 ---

def get_size_range_index(nominal_size):
    """
    根据公称尺寸返回尺寸段索引
    参数:
        nominal_size: 公称尺寸(mm)
    返回:
        尺寸段索引(0-12)，超出范围返回None
    """
    for i, (d_min, d_max) in enumerate(SIZE_RANGES):
        if d_min <= nominal_size <= d_max:
            return i
    return None


def get_geometric_mean(nominal_size):
    """
    计算尺寸段几何均值 D = sqrt(D1*D2)
    参数:
        nominal_size: 公称尺寸(mm)
    返回:
        几何均值D(mm)
    """
    idx = get_size_range_index(nominal_size)
    if idx is None:
        return None
    d_min, d_max = SIZE_RANGES[idx]
    if d_min == 0:
        # 第一个尺寸段(0~3mm)取特殊值
        return math.sqrt((0 + 3) / 2.0 * 3)
    return math.sqrt(d_min * d_max)


def get_it_value(nominal_size, grade_str):
    """
    查表获取IT公差值(微米)
    参数:
        nominal_size: 公称尺寸(mm)
        grade_str: 公差等级字符串，如 "IT6", "IT7"
    返回:
        公差值(微米)，查不到返回None
    """
    # 规范化等级字符串
    grade_str = grade_str.upper().replace("IT", "")
    key = "IT" + grade_str
    if key not in IT_VALUES:
        return None
    idx = get_size_range_index(nominal_size)
    if idx is None:
        return None
    return IT_VALUES[key][idx]


# --- 4.2 轴的基本偏差计算 ---

# j5-j8 轴的基本偏差查表值(微米)，对应13个尺寸段
SHAFT_J_VALUES = {
    "j5": [2, 3, 4, 5, 5, 6, 7, 8, 10, 11, 13, 14, 16],
    "j6": [4, 5, 6, 8, 9, 11, 13, 15, 18, 20, 22, 25, 28],
    "j7": [6, 8, 9, 11, 13, 16, 19, 22, 25, 29, 32, 36, 40],
    "j8": [8, 10, 12, 15, 18, 22, 26, 30, 35, 40, 45, 50, 55],
}


def calc_shaft_fundamental_deviation(letter, D, it_grade, nominal_size):
    """
    计算轴的基本偏差
    参数:
        letter: 基本偏差字母(小写)，如 a, b, c, ..., zc
        D: 几何均值(mm)
        it_grade: 公差等级数值(如6表示IT6)
        nominal_size: 公称尺寸(mm)，用于查表
    返回:
        (deviation_value_um, is_upper_deviation)
        deviation_value_um: 基本偏差值(微米)
        is_upper_deviation: True表示上偏差(es)，False表示下偏差(ei)
    """
    letter = letter.lower()

    # js: 对称分布，基本偏差 = IT/2
    if letter == "js":
        it_val = get_it_value(nominal_size, "IT" + str(it_grade))
        return it_val / 2.0, True  # 返回上偏差=+IT/2

    # j: 查表
    if letter == "j":
        grade_key = "j" + str(it_grade)
        if grade_key in SHAFT_J_VALUES:
            idx = get_size_range_index(nominal_size)
            if idx is not None:
                return float(SHAFT_J_VALUES[grade_key][idx]), True  # j的上偏差
        # 若查不到，用近似值
        it_val = get_it_value(nominal_size, "IT" + str(it_grade))
        return it_val * 0.3, True

    # a~h: 上偏差(es)为基本偏差
    if letter == "a":
        if D <= 120:
            es = -(265 + 1.3 * D)
        else:
            es = -3.5 * D
        return es, True

    if letter == "b":
        if D < 160:
            es = -(140 + 0.85 * D)
        else:
            es = -1.8 * D
        return es, True

    if letter == "c":
        if D <= 40:
            es = -52 * (D ** 0.2)
        else:
            es = -(95 + 0.8 * D)
        return es, True

    if letter == "d":
        es = -16 * (D ** 0.44)
        return es, True

    if letter == "e":
        es = -11 * (D ** 0.41)
        return es, True

    if letter == "f":
        es = -5.5 * (D ** 0.41)
        return es, True

    if letter == "g":
        es = -2.5 * (D ** 0.34)
        return es, True

    if letter == "h":
        return 0.0, True

    # cd, ef, fg: 取相邻两字母的几何均值
    if letter == "cd":
        es_a, _ = calc_shaft_fundamental_deviation("c", D, it_grade, nominal_size)
        es_d, _ = calc_shaft_fundamental_deviation("d", D, it_grade, nominal_size)
        es = math.sqrt(es_a * es_d)
        return es, True

    if letter == "ef":
        es_e, _ = calc_shaft_fundamental_deviation("e", D, it_grade, nominal_size)
        es_f, _ = calc_shaft_fundamental_deviation("f", D, it_grade, nominal_size)
        es = math.sqrt(es_e * es_f)
        return es, True

    if letter == "fg":
        es_f, _ = calc_shaft_fundamental_deviation("f", D, it_grade, nominal_size)
        es_g, _ = calc_shaft_fundamental_deviation("g", D, it_grade, nominal_size)
        es = math.sqrt(es_f * es_g)
        return es, True

    # k~zc: 下偏差(ei)为基本偏差
    if letter == "k":
        if it_grade <= 3 or it_grade >= 8:
            ei = 0.0
        else:
            # IT4~IT7
            ei = 0.6 * (D ** (1.0 / 3.0))
        return ei, False

    if letter == "m":
        # ei = +(IT7 - IT6)
        it7 = get_it_value(nominal_size, "IT7")
        it6 = get_it_value(nominal_size, "IT6")
        ei = it7 - it6
        return float(ei), False

    if letter == "n":
        ei = 5.0 * (D ** 0.34)
        return ei, False

    if letter == "p":
        # ISO 286: ei = IT7 + delta, delta depends on size range
        # More accurate: use lookup table for common sizes
        # Standard values (p5-p8) are slightly above IT7
        it7 = get_it_value(nominal_size, "IT7")
        # Add a small correction based on size (approximation of standard table)
        # For D > 0: ei ≈ IT7 + 0~5, using 0.07*D as approximation
        correction = max(0, min(5, round(0.07 * D)))
        ei = it7 + correction
        return float(ei), False

    if letter == "r":
        # ei = sqrt(p_val * s_val)
        p_val, _ = calc_shaft_fundamental_deviation("p", D, it_grade, nominal_size)
        s_val, _ = calc_shaft_fundamental_deviation("s", D, it_grade, nominal_size)
        ei = math.sqrt(abs(p_val * s_val))
        return ei, False

    if letter == "s":
        if D <= 50:
            it8 = get_it_value(nominal_size, "IT8")
            ei = it8 + 3.0
        else:
            it7 = get_it_value(nominal_size, "IT7")
            ei = it7 + 0.4 * D
        return float(ei), False

    if letter == "t":
        it7 = get_it_value(nominal_size, "IT7")
        ei = it7 + 0.63 * D
        return float(ei), False

    if letter == "u":
        it7 = get_it_value(nominal_size, "IT7")
        ei = it7 + D
        return float(ei), False

    if letter == "v":
        it7 = get_it_value(nominal_size, "IT7")
        ei = it7 + 1.25 * D
        return float(ei), False

    if letter == "x":
        it7 = get_it_value(nominal_size, "IT7")
        ei = it7 + 1.6 * D
        return float(ei), False

    if letter == "y":
        it7 = get_it_value(nominal_size, "IT7")
        ei = it7 + 2.0 * D
        return float(ei), False

    if letter == "z":
        it7 = get_it_value(nominal_size, "IT7")
        ei = it7 + 2.5 * D
        return float(ei), False

    if letter == "za":
        it8 = get_it_value(nominal_size, "IT8")
        ei = it8 + 3.15 * D
        return float(ei), False

    if letter == "zb":
        it9 = get_it_value(nominal_size, "IT9")
        ei = it9 + 4.0 * D
        return float(ei), False

    if letter == "zc":
        it10 = get_it_value(nominal_size, "IT10")
        ei = it10 + 4.0 * D
        return float(ei), False

    # 未知字母，返回0
    return 0.0, True


# --- 4.3 孔的基本偏差计算 ---

def calc_hole_fundamental_deviation(letter, D, it_grade, nominal_size):
    """
    计算孔的基本偏差
    通用规则: EI = -es (A~H), ES = -ei (K~ZC)
    特殊规则: J/K/M/N(IT<=8), P~ZC(IT<=7), D>3mm: ES = -ei + Delta
    其中 Delta = ITn - IT(n-1)
    参数:
        letter: 基本偏差字母(大写)，如 A, B, C, ..., ZC
        D: 几何均值(mm)
        it_grade: 公差等级数值
        nominal_size: 公称尺寸(mm)
    返回:
        (deviation_value_um, is_upper_deviation)
    """
    letter = letter.upper()

    # JS: 对称分布
    if letter == "JS":
        it_val = get_it_value(nominal_size, "IT" + str(it_grade))
        return it_val / 2.0, True

    # J: 查表近似
    if letter == "J":
        grade_key = "j" + str(it_grade)
        if grade_key in SHAFT_J_VALUES:
            idx = get_size_range_index(nominal_size)
            if idx is not None:
                return float(SHAFT_J_VALUES[grade_key][idx]), True
        it_val = get_it_value(nominal_size, "IT" + str(it_grade))
        return it_val * 0.3, True

    # A~H: 通用规则 EI = -es
    if letter in ["A", "B", "C", "D", "E", "F", "G", "H",
                   "CD", "EF", "FG"]:
        shaft_letter = letter.lower()
        shaft_es, _ = calc_shaft_fundamental_deviation(shaft_letter, D, it_grade, nominal_size)
        ei = -shaft_es  # 孔的下偏差 = -轴的上偏差
        return ei, False  # 返回下偏差

    # K~ZC: 判断是否需要特殊规则
    shaft_letter = letter.lower()
    shaft_ei, _ = calc_shaft_fundamental_deviation(shaft_letter, D, it_grade, nominal_size)

    # 特殊规则条件: J/K/M/N(IT<=8), P~ZC(IT<=7), D>3mm
    need_special = False
    if nominal_size > 3:
        if letter in ["J", "K", "M", "N"] and it_grade <= 8:
            need_special = True
        elif letter in ["P", "R", "S", "T", "U", "V", "X", "Y", "Z",
                        "ZA", "ZB", "ZC"] and it_grade <= 7:
            need_special = True

    if need_special:
        # 特殊规则: ES = -ei + Delta
        # Delta = ITn - IT(n-1)
        it_n = get_it_value(nominal_size, "IT" + str(it_grade))
        it_n_minus_1 = get_it_value(nominal_size, "IT" + str(it_grade - 1))
        if it_n is not None and it_n_minus_1 is not None:
            delta = it_n - it_n_minus_1
        else:
            delta = 0
        es = -shaft_ei + delta
        return es, True  # 返回上偏差
    else:
        # 通用规则: ES = -ei
        es = -shaft_ei
        return es, True  # 返回上偏差


# --- 4.4 公差查询函数 ---

def parse_designation(designation_str):
    """
    解析公差带代号，返回(字母, 等级, 类型)
    参数:
        designation_str: 公差带代号字符串，如 "H7", "f6"
    返回:
        (letter, grade, tol_type)
        letter: 基本偏差字母
        grade: 公差等级(整数)
        tol_type: "hole" 或 "shaft"
    """
    designation_str = designation_str.strip()
    # 匹配模式: 字母(可能2位) + 数字
    match = re.match(r'^([A-Za-z]{1,2})(\d+)$', designation_str)
    if not match:
        return None, None, None
    letter = match.group(1)
    grade = int(match.group(2))
    # 大写字母为孔，小写字母为轴
    if letter[0].isupper():
        return letter.upper(), grade, "hole"
    else:
        return letter.lower(), grade, "shaft"


def format_deviation(value_um):
    """
    格式化偏差值为工程字符串
    参数:
        value_um: 偏差值(微米)
    返回:
        格式化字符串，如 "+0.025", "-0.012", "0"
    """
    if value_um == 0:
        return "0"
    mm_val = value_um / 1000.0
    if mm_val > 0:
        return "+{:.3f}".format(mm_val).rstrip("0").rstrip(".")
    else:
        return "{:.3f}".format(mm_val).rstrip("0").rstrip(".")


def query_tolerance(designation, nominal_size):
    """
    查询公差带代号完整信息
    参数:
        designation: 公差带代号，如 "H7", "f6"
        nominal_size: 公称尺寸(mm)
    返回:
        dict 包含:
            designation: 代号
            type: "hole" 或 "shaft"
            ES: 上偏差(微米)
            EI: 下偏差(微米)
            IT: 公差值(微米)
            max_size: 最大极限尺寸(mm)
            min_size: 最小极限尺寸(mm)
    """
    letter, grade, tol_type = parse_designation(designation)
    if letter is None:
        return None

    # 获取IT公差值
    it_val = get_it_value(nominal_size, "IT" + str(grade))
    if it_val is None:
        return None

    # 获取几何均值
    D = get_geometric_mean(nominal_size)
    if D is None:
        return None

    if tol_type == "shaft":
        # 轴: 计算基本偏差
        dev_val, is_upper = calc_shaft_fundamental_deviation(
            letter, D, grade, nominal_size
        )
        if is_upper:
            # es为基本偏差
            es = dev_val
            ei = es - it_val
        else:
            # ei为基本偏差
            ei = dev_val
            es = ei + it_val
    else:
        # 孔: 计算基本偏差
        dev_val, is_upper = calc_hole_fundamental_deviation(
            letter, D, grade, nominal_size
        )
        if is_upper:
            # ES为基本偏差
            es = dev_val
            ei = es - it_val
        else:
            # EI为基本偏差
            ei = dev_val
            es = ei + it_val

    # 消除 -0.0 的浮点精度问题
    if abs(es) < 1e-10:
        es = 0.0
    if abs(ei) < 1e-10:
        ei = 0.0

    return {
        "designation": designation,
        "type": tol_type,
        "ES": es,
        "EI": ei,
        "IT": it_val,
        "max_size": nominal_size + es / 1000.0,
        "min_size": nominal_size + ei / 1000.0,
    }


# ============================================================
# 第5节：尺寸链计算
# ============================================================

def calculate_dimension_chain(components):
    """
    极值法计算尺寸链
    参数:
        components: 组成环列表，每个元素为字典:
            - name: 环名称
            - basic_size: 基本尺寸(mm)
            - upper_dev: 上偏差(mm)
            - lower_dev: 下偏差(mm)
            - ring_type: "增环" 或 "减环"
    返回:
        dict 包含:
            A0: 封闭环基本尺寸(mm)
            ES0: 封闭环上偏差(mm)
            EI0: 封闭环下偏差(mm)
            T0: 封闭环公差(mm)
            A0_max: 封闭环最大极限尺寸(mm)
            A0_min: 封闭环最小极限尺寸(mm)
            details: 计算过程描述
            contributions: 各组成环贡献列表
    """
    # 计算封闭环基本尺寸
    A0 = 0.0
    for comp in components:
        if comp["ring_type"] == "增环":
            A0 += comp["basic_size"]
        else:
            A0 -= comp["basic_size"]

    # 计算封闭环上偏差
    ES0 = 0.0
    for comp in components:
        if comp["ring_type"] == "增环":
            ES0 += comp["upper_dev"]
        else:
            ES0 -= comp["lower_dev"]

    # 计算封闭环下偏差
    EI0 = 0.0
    for comp in components:
        if comp["ring_type"] == "增环":
            EI0 += comp["lower_dev"]
        else:
            EI0 -= comp["upper_dev"]

    # 封闭环公差
    T0 = ES0 - EI0

    # 极限尺寸
    A0_max = A0 + ES0
    A0_min = A0 + EI0

    # 构建计算过程描述
    detail_lines = []
    detail_lines.append("=== 极值法尺寸链计算 ===")
    detail_lines.append("")

    # 列出各组成环
    detail_lines.append("【组成环】")
    for comp in components:
        symbol = "+" if comp["ring_type"] == "增环" else "-"
        detail_lines.append(
            "  {} {} = {} ({:+.3f}/{:+.3f})".format(
                comp["ring_type"],
                comp["name"],
                comp["basic_size"],
                comp["upper_dev"],
                comp["lower_dev"],
            )
        )
    detail_lines.append("")

    # 基本尺寸计算
    increasing_sizes = [c["basic_size"] for c in components if c["ring_type"] == "增环"]
    decreasing_sizes = [c["basic_size"] for c in components if c["ring_type"] == "减环"]
    detail_lines.append("【封闭环基本尺寸】")
    detail_lines.append(
        "  A0 = Σ(增环) - Σ(减环) = {} - {} = {:.3f} mm".format(
            " + ".join(str(s) for s in increasing_sizes) if increasing_sizes else "0",
            " + ".join(str(s) for s in decreasing_sizes) if decreasing_sizes else "0",
            A0,
        )
    )
    detail_lines.append("")

    # 上偏差计算
    detail_lines.append("【封闭环上偏差】")
    es_parts_inc = []
    es_parts_dec = []
    for comp in components:
        if comp["ring_type"] == "增环":
            es_parts_inc.append("{:+.3f}".format(comp["upper_dev"]))
        else:
            es_parts_dec.append("{:+.3f}".format(comp["lower_dev"]))
    detail_lines.append(
        "  ES0 = Σ(增环ES) - Σ(减环EI) = ({}) - ({}) = {:+.3f} mm".format(
            " + ".join(es_parts_inc) if es_parts_inc else "0",
            " + ".join(es_parts_dec) if es_parts_dec else "0",
            ES0,
        )
    )
    detail_lines.append("")

    # 下偏差计算
    detail_lines.append("【封闭环下偏差】")
    ei_parts_inc = []
    ei_parts_dec = []
    for comp in components:
        if comp["ring_type"] == "增环":
            ei_parts_inc.append("{:+.3f}".format(comp["lower_dev"]))
        else:
            ei_parts_dec.append("{:+.3f}".format(comp["upper_dev"]))
    detail_lines.append(
        "  EI0 = Σ(增环EI) - Σ(减环ES) = ({}) - ({}) = {:+.3f} mm".format(
            " + ".join(ei_parts_inc) if ei_parts_inc else "0",
            " + ".join(ei_parts_dec) if ei_parts_dec else "0",
            EI0,
        )
    )
    detail_lines.append("")

    # 公差
    detail_lines.append("【封闭环公差】")
    detail_lines.append("  T0 = ES0 - EI0 = {:+.3f} - ({:+.3f}) = {:.3f} mm".format(
        ES0, EI0, T0
    ))
    detail_lines.append("")

    # 极限尺寸
    detail_lines.append("【封闭环极限尺寸】")
    detail_lines.append("  A0_max = A0 + ES0 = {:.3f} + {:+.3f} = {:.3f} mm".format(
        A0, ES0, A0_max
    ))
    detail_lines.append("  A0_min = A0 + EI0 = {:.3f} + {:+.3f} = {:.3f} mm".format(
        A0, EI0, A0_min
    ))

    # 各组成环贡献
    contributions = []
    for comp in components:
        comp_tol = comp["upper_dev"] - comp["lower_dev"]
        contributions.append({
            "name": comp["name"],
            "ring_type": comp["ring_type"],
            "basic_size": comp["basic_size"],
            "tolerance": comp_tol,
            "contribution": "增加封闭环公差" if comp["ring_type"] == "增环" else "增加封闭环公差",
        })

    return {
        "A0": A0,
        "ES0": ES0,
        "EI0": EI0,
        "T0": T0,
        "A0_max": A0_max,
        "A0_min": A0_min,
        "details": "\n".join(detail_lines),
        "contributions": contributions,
    }


# ============================================================
# 第6节：形位公差查询辅助函数
# ============================================================

def lookup_geo_tolerance(item_name, grade, param_value):
    """
    根据公差项目名称、等级和主参数值查询形位公差值
    参数:
        item_name: 公差项目名称，如 "圆度", "圆柱度", "直线度", "平面度", "平行度", "垂直度", "同轴度", "对称度", "圆跳动" 等
        grade: 公差等级(整数)
        param_value: 主参数值(mm)
    返回:
        公差值(微米)，查不到返回None
    """
    grade = int(grade)

    # 圆度、圆柱度 - 按直径范围查表
    if item_name in ["圆度", "圆柱度"]:
        if grade not in CIRCULARITY_VALUES:
            return None
        for i, (d_min, d_max) in enumerate(CIRCULARITY_DIAMETER_RANGES):
            if d_min <= param_value <= d_max:
                return CIRCULARITY_VALUES[grade][i]
        return None

    # 直线度、平面度 - 按长度范围查表
    if item_name in ["直线度", "平面度"]:
        if grade not in STRAIGHTNESS_VALUES:
            return None
        for i, (d_min, d_max) in enumerate(STRAIGHTNESS_LENGTH_RANGES):
            if d_min <= param_value <= d_max:
                return STRAIGHTNESS_VALUES[grade][i]
        return None

    # 平行度、垂直度 - 按长度范围查表
    if item_name in ["平行度", "垂直度"]:
        if grade not in PARALLELISM_VALUES:
            return None
        for i, (d_min, d_max) in enumerate(PARALLELISM_LENGTH_RANGES):
            if d_min <= param_value <= d_max:
                return PARALLELISM_VALUES[grade][i]
        return None

    # 同轴度、对称度、圆跳动 - 按直径范围查表
    if item_name in ["同轴度", "对称度", "圆跳动", "端面跳动", "全跳动"]:
        if grade not in COAXIALITY_VALUES:
            return None
        for i, (d_min, d_max) in enumerate(COAXIALITY_DIAMETER_RANGES):
            if d_min <= param_value <= d_max:
                return COAXIALITY_VALUES[grade][i]
        return None

    # 位置度 - 按直径范围查表，使用同轴度表近似
    if item_name == "位置度":
        if grade not in COAXIALITY_VALUES:
            return None
        for i, (d_min, d_max) in enumerate(COAXIALITY_DIAMETER_RANGES):
            if d_min <= param_value <= d_max:
                return COAXIALITY_VALUES[grade][i]
        return None

    return None


# ============================================================
# 第7节：尺寸链计算界面渲染函数
# ============================================================

def render_dimension_chain_tab():
    """渲染尺寸链计算选项卡"""
    st.markdown("## 📏 尺寸链计算（极值法）")

    # 初始化session_state中的组成环列表
    if "dim_chain_components" not in st.session_state:
        st.session_state.dim_chain_components = [
            {"name": "A1", "basic_size": 50.0, "upper_dev": 0.0, "lower_dev": -0.1, "ring_type": "增环"},
            {"name": "A2", "basic_size": 30.0, "upper_dev": 0.05, "lower_dev": -0.05, "ring_type": "减环"},
            {"name": "A3", "basic_size": 20.0, "upper_dev": 0.05, "lower_dev": -0.05, "ring_type": "增环"},
        ]

    # 显示各组成环输入行
    st.markdown("### 输入组成环")
    cols_header = st.columns([2, 2, 2, 2, 2, 1])
    cols_header[0].markdown("**名称**")
    cols_header[1].markdown("**基本尺寸(mm)**")
    cols_header[2].markdown("**上偏差(mm)**")
    cols_header[3].markdown("**下偏差(mm)**")
    cols_header[4].markdown("**环类型**")
    cols_header[5].markdown("**操作**")

    components_to_remove = []
    for i, comp in enumerate(st.session_state.dim_chain_components):
        cols = st.columns([2, 2, 2, 2, 2, 1])
        comp["name"] = cols[0].text_input("名称", value=comp["name"], key=f"comp_name_{i}", label_visibility="collapsed")
        comp["basic_size"] = cols[1].number_input("基本尺寸", value=comp["basic_size"], key=f"comp_size_{i}", label_visibility="collapsed", step=0.1)
        comp["upper_dev"] = cols[2].number_input("上偏差", value=comp["upper_dev"], key=f"comp_upper_{i}", label_visibility="collapsed", step=0.001, format="%.3f")
        comp["lower_dev"] = cols[3].number_input("下偏差", value=comp["lower_dev"], key=f"comp_lower_{i}", label_visibility="collapsed", step=0.001, format="%.3f")
        comp["ring_type"] = cols[4].selectbox("环类型", options=["增环", "减环"], index=0 if comp["ring_type"] == "增环" else 1, key=f"comp_type_{i}", label_visibility="collapsed")
        if cols[5].button("删除", key=f"comp_del_{i}"):
            components_to_remove.append(i)

    # 删除标记的组成环
    if components_to_remove:
        st.session_state.dim_chain_components = [
            c for i, c in enumerate(st.session_state.dim_chain_components)
            if i not in components_to_remove
        ]
        st.rerun()

    # 添加组成环按钮
    col_add, col_info = st.columns([1, 3])
    if col_add.button("➕ 添加组成环", disabled=len(st.session_state.dim_chain_components) >= 10, key="add_comp_btn"):
        n = len(st.session_state.dim_chain_components) + 1
        st.session_state.dim_chain_components.append({
            "name": f"A{n}",
            "basic_size": 10.0,
            "upper_dev": 0.0,
            "lower_dev": -0.1,
            "ring_type": "增环",
        })
        st.rerun()
    if len(st.session_state.dim_chain_components) >= 10:
        col_info.warning("最多支持10个组成环")

    st.markdown("---")

    # 开始计算按钮
    if st.button("🚀 开始计算", type="primary", use_container_width=True):
        components = st.session_state.dim_chain_components

        # 输入验证
        has_error = False
        for comp in components:
            if comp["basic_size"] <= 0:
                st.error(f"组成环 {comp['name']} 的基本尺寸必须大于0")
                has_error = True
            if comp["upper_dev"] < comp["lower_dev"]:
                st.error(f"组成环 {comp['name']} 的上偏差({comp['upper_dev']})不能小于下偏差({comp['lower_dev']})")
                has_error = True
            if not comp["name"].strip():
                st.error("所有组成环必须有名称")
                has_error = True

        if has_error:
            return

        # 执行计算
        result = calculate_dimension_chain(components)

        # 显示结果
        st.markdown("### 计算结果")
        st.success("尺寸链计算完成")

        # 4个指标卡片
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("封闭环基本尺寸", f"{result['A0']:.3f} mm")
        col2.metric("上偏差", f"{result['ES0']:+.3f} mm")
        col3.metric("下偏差", f"{result['EI0']:+.3f} mm")
        col4.metric("公差值", f"{result['T0']:.3f} mm")

        # 组成环详情表格
        st.markdown("#### 组成环详情")
        table_data = []
        for c in result["contributions"]:
            table_data.append({
                "名称": c["name"],
                "环类型": c["ring_type"],
                "基本尺寸(mm)": c["basic_size"],
                "公差(mm)": f"{c['tolerance']:.3f}",
                "贡献": c["contribution"],
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 计算过程
        st.markdown("#### 计算过程")
        st.code(result["details"], language="text")

        # 复制结果按钮
        copy_text = (
            f"=== 尺寸链计算结果 ===\n"
            f"封闭环基本尺寸: {result['A0']:.3f} mm\n"
            f"上偏差: {result['ES0']:+.3f} mm\n"
            f"下偏差: {result['EI0']:+.3f} mm\n"
            f"公差值: {result['T0']:.3f} mm\n"
            f"最大极限尺寸: {result['A0_max']:.3f} mm\n"
            f"最小极限尺寸: {result['A0_min']:.3f} mm\n"
            f"\n{result['details']}"
        )
        st.code(copy_text, language="text")


# ============================================================
# 第8节：公差查询界面渲染函数
# ============================================================

def render_tolerance_query_tab():
    """渲染公差查询选项卡"""
    st.markdown("## 🔍 公差查询")

    # 输入区域
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    nominal_size = col1.number_input("公称尺寸 (mm)", value=50.0, min_value=0.1, max_value=500.0, step=0.1)
    hole_designation = col2.text_input("孔公差带代号", value="H7", placeholder="如 H7")
    shaft_designation = col3.text_input("轴公差带代号", value="f6", placeholder="如 f6")
    query_btn = col4.button("🔍 查询")

    if query_btn:
        hole_info = None
        shaft_info = None

        # 查询孔公差
        if hole_designation.strip():
            hole_info = query_tolerance(hole_designation.strip(), nominal_size)
            if hole_info is None:
                st.error(f"孔公差带代号 '{hole_designation}' 无效或公称尺寸超出范围")

        # 查询轴公差
        if shaft_designation.strip():
            shaft_info = query_tolerance(shaft_designation.strip(), nominal_size)
            if shaft_info is None:
                st.error(f"轴公差带代号 '{shaft_designation}' 无效或公称尺寸超出范围")

        if hole_info is None and shaft_info is None:
            st.warning("请至少输入一个有效的公差带代号")
            return

        # 同时提供孔和轴信息时，显示配合分析
        if hole_info is not None and shaft_info is not None:
            st.markdown("### 查询结果")

            # 两列显示孔和轴信息
            col_h, col_s = st.columns(2)

            with col_h:
                st.markdown("#### 🔴 孔信息")
                st.metric("代号", hole_info["designation"])
                st.write(f"**上偏差 (ES):** {format_deviation(hole_info['ES'])} mm")
                st.write(f"**下偏差 (EI):** {format_deviation(hole_info['EI'])} mm")
                st.write(f"**公差 (IT):** {hole_info['IT']} μm = {hole_info['IT']/1000:.3f} mm")
                st.write(f"**最大极限尺寸:** {hole_info['max_size']:.3f} mm")
                st.write(f"**最小极限尺寸:** {hole_info['min_size']:.3f} mm")

            with col_s:
                st.markdown("#### 🔵 轴信息")
                st.metric("代号", shaft_info["designation"])
                st.write(f"**上偏差 (es):** {format_deviation(shaft_info['ES'])} mm")
                st.write(f"**下偏差 (ei):** {format_deviation(shaft_info['EI'])} mm")
                st.write(f"**公差 (IT):** {shaft_info['IT']} μm = {shaft_info['IT']/1000:.3f} mm")
                st.write(f"**最大极限尺寸:** {shaft_info['max_size']:.3f} mm")
                st.write(f"**最小极限尺寸:** {shaft_info['min_size']:.3f} mm")

            # 配合分析
            st.markdown("---")
            st.markdown("#### 配合分析")

            # 最大间隙 = 孔最大 - 轴最小
            max_clearance = hole_info["max_size"] - shaft_info["min_size"]
            # 最小间隙 / 最大过盈 = 孔最小 - 轴最大
            min_clearance_max_interference = hole_info["min_size"] - shaft_info["max_size"]

            if min_clearance_max_interference >= 0:
                fit_type = "间隙配合"
                st.success(f"**配合类型:** {fit_type}")
                st.write(f"**最大间隙 (X_max):** {max_clearance*1000:.1f} μm = {max_clearance:.3f} mm")
                st.write(f"**最小间隙 (X_min):** {min_clearance_max_interference*1000:.1f} μm = {min_clearance_max_interference:.3f} mm")
            elif max_clearance <= 0:
                fit_type = "过盈配合"
                st.error(f"**配合类型:** {fit_type}")
                st.write(f"**最大过盈 (Y_max):** {abs(min_clearance_max_interference)*1000:.1f} μm = {abs(min_clearance_max_interference):.3f} mm")
                st.write(f"**最小过盈 (Y_min):** {abs(max_clearance)*1000:.1f} μm = {abs(max_clearance):.3f} mm")
            else:
                fit_type = "过渡配合"
                st.warning(f"**配合类型:** {fit_type}")
                st.write(f"**最大间隙 (X_max):** {max_clearance*1000:.1f} μm = {max_clearance:.3f} mm")
                st.write(f"**最大过盈 (Y_max):** {abs(min_clearance_max_interference)*1000:.1f} μm = {abs(min_clearance_max_interference):.3f} mm")

            # 查找常用配合信息
            fit_key_hole = hole_info["designation"].upper()
            fit_key_shaft = shaft_info["designation"].lower()
            fit_key = f"{fit_key_hole}/{fit_key_shaft}"
            # 也尝试基轴制形式
            fit_key_alt = None
            if shaft_info["designation"].lower() == "h6":
                # 基轴制: 查找 孔大写/轴小写
                pass
            # 尝试多种组合
            possible_keys = [
                f"{fit_key_hole}/{fit_key_shaft}",
                f"{fit_key_hole}/{shaft_info['designation']}",
            ]

            fit_info_found = None
            for key in possible_keys:
                if key in COMMON_FITS_INFO:
                    fit_info_found = COMMON_FITS_INFO[key]
                    break

            if fit_info_found:
                st.markdown("#### 应用场景")
                st.info(fit_info_found["description"])
                st.write("**典型应用:**")
                for app in fit_info_found["applications"]:
                    st.write(f"- {app}")
                st.write(f"**装配方式:** {fit_info_found['assembly']}")

            st.caption("数据来源: GB/T 1800.1-2020, GB/T 1801-2009")

            # 复制结果
            copy_text = (
                f"=== 公差查询结果 ===\n"
                f"公称尺寸: {nominal_size} mm\n"
                f"\n孔: {hole_info['designation']}\n"
                f"  ES = {format_deviation(hole_info['ES'])} mm\n"
                f"  EI = {format_deviation(hole_info['EI'])} mm\n"
                f"  IT = {hole_info['IT']} μm\n"
                f"  最大尺寸: {hole_info['max_size']:.3f} mm\n"
                f"  最小尺寸: {hole_info['min_size']:.3f} mm\n"
                f"\n轴: {shaft_info['designation']}\n"
                f"  es = {format_deviation(shaft_info['ES'])} mm\n"
                f"  ei = {format_deviation(shaft_info['EI'])} mm\n"
                f"  IT = {shaft_info['IT']} μm\n"
                f"  最大尺寸: {shaft_info['max_size']:.3f} mm\n"
                f"  最小尺寸: {shaft_info['min_size']:.3f} mm\n"
                f"\n配合类型: {fit_type}\n"
            )
            if fit_info_found:
                copy_text += f"说明: {fit_info_found['description']}\n"
                copy_text += f"装配方式: {fit_info_found['assembly']}\n"
            st.code(copy_text, language="text")

        else:
            # 只提供一个公差带代号
            st.markdown("### 查询结果")
            info = hole_info if hole_info else shaft_info
            type_label = "孔" if info["type"] == "hole" else "轴"
            es_label = "ES" if info["type"] == "hole" else "es"
            ei_label = "EI" if info["type"] == "hole" else "ei"

            st.metric(f"{type_label}公差带代号", info["designation"])
            st.write(f"**{es_label} (上偏差):** {format_deviation(info['ES'])} mm")
            st.write(f"**{ei_label} (下偏差):** {format_deviation(info['EI'])} mm")
            st.write(f"**公差 (IT):** {info['IT']} μm = {info['IT']/1000:.3f} mm")
            st.write(f"**最大极限尺寸:** {info['max_size']:.3f} mm")
            st.write(f"**最小极限尺寸:** {info['min_size']:.3f} mm")

            copy_text = (
                f"=== 公差查询结果 ===\n"
                f"公称尺寸: {nominal_size} mm\n"
                f"{type_label}: {info['designation']}\n"
                f"  {es_label} = {format_deviation(info['ES'])} mm\n"
                f"  {ei_label} = {format_deviation(info['EI'])} mm\n"
                f"  IT = {info['IT']} μm\n"
                f"  最大尺寸: {info['max_size']:.3f} mm\n"
                f"  最小尺寸: {info['min_size']:.3f} mm\n"
            )
            st.code(copy_text, language="text")

    # IT等级参考表
    with st.expander("📖 IT等级参考表"):
        st.markdown("标准公差等级 (GB/T 1800.1-2020)")
        # 构建参考表
        it_ref_data = []
        for grade_name in ["IT01", "IT0", "IT1", "IT2", "IT3", "IT4", "IT5", "IT6", "IT7", "IT8", "IT9", "IT10", "IT11", "IT12"]:
            vals = IT_VALUES[grade_name]
            # 取中间尺寸段(30-50mm)的值作为参考
            it_ref_data.append({
                "等级": grade_name,
                "0~3mm": vals[0],
                "3~6mm": vals[1],
                "6~10mm": vals[2],
                "10~18mm": vals[3],
                "18~30mm": vals[4],
                "30~50mm": vals[5],
                "50~80mm": vals[6],
                "80~120mm": vals[7],
                "120~180mm": vals[8],
                "180~250mm": vals[9],
            })
        df_it = pd.DataFrame(it_ref_data)
        st.dataframe(df_it, use_container_width=True, hide_index=True)
        st.caption("单位: 微米 (μm)")


# ============================================================
# 第9节：配合推荐界面渲染函数
# ============================================================

def render_fit_recommendation_tab():
    """渲染配合推荐选项卡"""
    st.markdown("## 🎯 公差配合推荐")

    with st.form("fit_recommendation_form"):
        col1, col2 = st.columns(2)
        fit_type = col1.selectbox("配合类型", options=["轴孔配合"], index=0)
        basic_size = col2.number_input("基本尺寸 (mm)", value=50.0, min_value=0.1, max_value=500.0, step=0.1)

        col3, col4, col5 = st.columns(3)
        load_level = col3.selectbox("载荷等级", options=["轻载", "中载", "重载"], index=0)
        speed_level = col4.selectbox("转速等级", options=["低速", "中速", "高速"], index=0)
        precision_level = col5.selectbox("定心精度", options=["一般", "较高", "高精度"], index=0)

        col6, col7 = st.columns(2)
        disassembly_req = col6.selectbox("拆卸要求", options=["频繁拆卸", "偶尔拆卸", "不拆卸", "永久装配", "自由装配"], index=0)
        system_basis = col7.selectbox("优先制度", options=["基孔制", "基轴制"], index=0)

        submitted = st.form_submit_button("🔍 获取推荐配合", type="primary", use_container_width=True)

    if submitted:
        # 推荐引擎：匹配规则
        user_conditions = {
            "load": load_level,
            "speed": speed_level,
            "precision": precision_level,
            "disassembly": disassembly_req,
        }

        scored_rules = []
        for rule in FIT_RECOMMENDATION_RULES:
            match_count = 0
            total_conditions = len(rule["conditions"])
            for key, value in rule["conditions"].items():
                if key in user_conditions and user_conditions[key] == value:
                    match_count += 1
            scored_rules.append({
                "rule": rule,
                "match_count": match_count,
                "match_ratio": match_count / total_conditions if total_conditions > 0 else 0,
            })

        # 按匹配数排序，取前3
        scored_rules.sort(key=lambda x: x["match_count"], reverse=True)
        top_rules = scored_rules[:3]

        if not top_rules or top_rules[0]["match_count"] == 0:
            st.warning("未找到完全匹配的推荐规则，以下为最接近的推荐：")

        # 收集所有推荐的配合代号（去重）
        all_recommended_fits = []
        seen_fits = set()
        for sr in top_rules:
            for fit in sr["rule"]["fits"]:
                if fit not in seen_fits:
                    all_recommended_fits.append({
                        "fit": fit,
                        "rule": sr["rule"],
                        "match_count": sr["match_count"],
                    })
                    seen_fits.add(fit)

        # 显示推荐结果
        for idx, rec in enumerate(all_recommended_fits[:3]):
            fit_designation = rec["fit"]
            rule = rec["rule"]

            st.markdown(f"### 推荐 {idx + 1}: {fit_designation}")

            # 查询实际偏差值
            hole_letter = fit_designation[0].upper()
            shaft_letter = fit_designation.split("/")[1][0].lower() if "/" in fit_designation else None

            # 解析配合代号
            parts = fit_designation.split("/")
            hole_desig = parts[0] if len(parts) > 0 else None
            shaft_desig = parts[1] if len(parts) > 1 else None

            col_info, col_detail = st.columns([1, 1])

            with col_info:
                # 从COMMON_FITS_INFO获取信息
                if fit_designation in COMMON_FITS_INFO:
                    fit_info = COMMON_FITS_INFO[fit_designation]
                    st.info(f"**类型:** {fit_info['type']}")
                    st.write(f"**说明:** {fit_info['description']}")
                    st.write(f"**装配方式:** {fit_info['assembly']}")
                else:
                    st.info("配合信息")

                st.write(f"**匹配条件:** {rec['match_count']}/{len(rule['conditions'])}")
                st.write(f"**推荐理由:** {rule['reason']}")

            with col_detail:
                # 计算实际偏差值
                if hole_desig and shaft_desig:
                    hole_result = query_tolerance(hole_desig, basic_size)
                    shaft_result = query_tolerance(shaft_desig, basic_size)

                    if hole_result and shaft_result:
                        st.markdown("**实际偏差值:**")
                        st.write(f"孔 {hole_desig}: ES={format_deviation(hole_result['ES'])}, EI={format_deviation(hole_result['EI'])}")
                        st.write(f"轴 {shaft_desig}: es={format_deviation(shaft_result['ES'])}, ei={format_deviation(shaft_result['EI'])}")

                        max_clearance = hole_result["max_size"] - shaft_result["min_size"]
                        min_clearance_max_int = hole_result["min_size"] - shaft_result["max_size"]

                        if min_clearance_max_int >= 0:
                            st.write(f"最大间隙: {max_clearance*1000:.1f} μm")
                            st.write(f"最小间隙: {min_clearance_max_int*1000:.1f} μm")
                        elif max_clearance <= 0:
                            st.write(f"最大过盈: {abs(min_clearance_max_int)*1000:.1f} μm")
                            st.write(f"最小过盈: {abs(max_clearance)*1000:.1f} μm")
                        else:
                            st.write(f"最大间隙: {max_clearance*1000:.1f} μm")
                            st.write(f"最大过盈: {abs(min_clearance_max_int)*1000:.1f} μm")

                # 推荐表面粗糙度
                st.markdown("**推荐表面粗糙度:**")
                if hole_result:
                    hole_grade = int(hole_desig[1:]) if len(hole_desig) > 1 else 7
                    if hole_grade <= 5:
                        ra_hole = "0.4~0.8"
                    elif hole_grade <= 7:
                        ra_hole = "0.8~1.6"
                    elif hole_grade <= 9:
                        ra_hole = "1.6~3.2"
                    else:
                        ra_hole = "3.2~6.3"
                    st.write(f"孔: Ra {ra_hole} μm")

                if shaft_result:
                    shaft_grade = int(shaft_desig[1:]) if len(shaft_desig) > 1 else 6
                    if shaft_grade <= 5:
                        ra_shaft = "0.2~0.4"
                    elif shaft_grade <= 7:
                        ra_shaft = "0.4~0.8"
                    elif shaft_grade <= 9:
                        ra_shaft = "0.8~1.6"
                    else:
                        ra_shaft = "1.6~3.2"
                    st.write(f"轴: Ra {ra_shaft} μm")

                # 推荐形位公差
                st.markdown("**推荐形位公差:**")
                st.write("- 圆柱度: 6~8级")
                st.write("- 同轴度: 6~8级")
                st.write("- 圆跳动: 7~9级")

            st.markdown("---")

        # 复制所有推荐
        copy_lines = ["=== 公差配合推荐结果 ==="]
        copy_lines.append(f"基本尺寸: {basic_size} mm")
        copy_lines.append(f"载荷: {load_level}, 转速: {speed_level}, 精度: {precision_level}")
        copy_lines.append(f"拆卸要求: {disassembly_req}, 制度: {system_basis}")
        copy_lines.append("")
        for idx, rec in enumerate(all_recommended_fits[:3]):
            fit_designation = rec["fit"]
            copy_lines.append(f"推荐{idx+1}: {fit_designation}")
            copy_lines.append(f"  推荐理由: {rec['rule']['reason']}")
            if fit_designation in COMMON_FITS_INFO:
                fi = COMMON_FITS_INFO[fit_designation]
                copy_lines.append(f"  类型: {fi['type']}")
                copy_lines.append(f"  说明: {fi['description']}")
                copy_lines.append(f"  装配方式: {fi['assembly']}")
            copy_lines.append("")

        st.code("\n".join(copy_lines), language="text")

    # 常用配合参考表
    with st.expander("📖 常用配合参考表"):
        ref_data = []
        for key, info in COMMON_FITS_INFO.items():
            ref_data.append({
                "配合代号": key,
                "类型": info["type"],
                "说明": info["description"],
                "装配方式": info["assembly"],
            })
        df_ref = pd.DataFrame(ref_data)
        st.dataframe(df_ref, use_container_width=True, hide_index=True)


# ============================================================
# 第10节：形位公差查询界面渲染函数
# ============================================================

def render_geometric_tolerance_tab():
    """渲染形位公差查询选项卡"""
    st.markdown("## 📐 形位公差推荐")

    # 输入区域
    col1, col2, col3, col4 = st.columns(4)
    part_type = col1.selectbox("零件类型", options=["轴", "孔", "箱体", "法兰", "端盖"], index=0)

    # 根据零件类型动态填充功能选项
    if part_type in GEOMETRIC_TOLERANCE_RECOMMENDATIONS:
        functions = list(GEOMETRIC_TOLERANCE_RECOMMENDATIONS[part_type].keys())
    else:
        functions = []
    part_function = col2.selectbox("主要功能", options=functions, index=0 if functions else None)
    precision_level = col3.selectbox("精度等级", options=["一般", "较高", "很高"], index=0)
    param_value = col4.number_input("主参数值 (mm)", value=50.0, min_value=0.01, max_value=1000.0, step=1.0)

    # 查询按钮
    if st.button("🔍 获取形位公差推荐", type="primary", use_container_width=True):
        if not functions:
            st.warning(f"未找到 '{part_type}' 的推荐数据")
            return

        recommendations = GEOMETRIC_TOLERANCE_RECOMMENDATIONS[part_type].get(part_function, [])
        if not recommendations:
            st.warning(f"未找到 '{part_type} - {part_function}' 的推荐数据")
            return

        st.markdown("### 推荐结果")

        # 精度等级调整
        grade_adjust = {"一般": 0, "较高": -1, "很高": -2}
        adjust = grade_adjust.get(precision_level, 0)

        for idx, rec in enumerate(recommendations):
            item_name = rec["item"]
            base_grade_min, base_grade_max = rec["grade_range"]

            # 根据精度等级调整推荐等级范围
            adj_grade_min = max(1, base_grade_min + adjust)
            adj_grade_max = max(1, base_grade_max + adjust)

            # 查询公差值（取中间等级）
            mid_grade = (adj_grade_min + adj_grade_max) // 2
            tol_value = lookup_geo_tolerance(item_name, mid_grade, param_value)

            with st.container():
                col_name, col_grade, col_value, col_reason = st.columns([2, 2, 2, 4])

                col_name.markdown(f"**{idx + 1}. {item_name}**")
                col_grade.write(f"推荐等级: {adj_grade_min}~{adj_grade_max} 级")
                if tol_value is not None:
                    col_value.metric(f"{item_name}公差值", f"{tol_value} μm")
                else:
                    col_value.write("公差值: 无法查询（参数超出范围）")
                col_reason.info(rec["reason"])

                # 标注位置和方法建议
                st.caption(f"📌 标注建议: 在{part_type}的{part_function}处标注{item_name}，推荐等级{adj_grade_min}~{adj_grade_max}级")

            st.markdown("---")

    # 手动查询形位公差
    with st.expander("🔧 手动查询形位公差值"):
        geo_col1, geo_col2, geo_col3 = st.columns(3)
        geo_item_options = ["圆度", "圆柱度", "直线度", "平面度", "平行度", "垂直度", "同轴度", "对称度", "圆跳动", "位置度"]
        selected_geo_item = geo_col1.selectbox("公差项目", options=geo_item_options)
        selected_geo_grade = geo_col2.selectbox("公差等级", options=list(range(1, 13)), index=5)
        selected_geo_param = geo_col3.number_input("主参数值 (mm)", value=50.0, min_value=0.01, max_value=1000.0, step=1.0, key="geo_param")

        geo_tol = lookup_geo_tolerance(selected_geo_item, selected_geo_grade, selected_geo_param)
        if geo_tol is not None:
            st.success(f"**{selected_geo_item}** (等级{selected_geo_grade}, 参数{selected_geo_param}mm): **{geo_tol} μm**")
        else:
            st.error("无法查询，请检查参数值是否在有效范围内")


# ============================================================
# 第11节：主函数
# ============================================================

def main():
    """主函数：构建Streamlit应用界面"""
    # 页面标题
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ 机械公差助手</h1>
        <p>基于 GB/T 1800.1-2020 / GB/T 1801-2009 / GB/T 1184-1996 国家标准 | v1.0</p>
    </div>
    """, unsafe_allow_html=True)

    # 创建选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "📏 尺寸链计算",
        "🔍 公差查询",
        "🎯 公差配合推荐",
        "📐 形位公差推荐",
    ])

    with tab1:
        render_dimension_chain_tab()

    with tab2:
        render_tolerance_query_tab()

    with tab3:
        render_fit_recommendation_tab()

    with tab4:
        render_geometric_tolerance_tab()

    # 页脚免责声明
    st.markdown("""
    <div class="disclaimer">
        ⚠️ 免责声明：本工具计算结果仅供参考，关键设计请以国家标准和设计手册为准。
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    main()
