# -*- coding: utf-8 -*-
"""
工具函数模块
包含：核心计算函数、SVG生成函数、公差查询辅助函数
"""

import math
import re

from data.tolerance_data import (
    SIZE_RANGES, IT_VALUES, SHAFT_J_VALUES,
    CIRCULARITY_DIAMETER_RANGES, CIRCULARITY_VALUES,
    STRAIGHTNESS_LENGTH_RANGES, STRAIGHTNESS_VALUES,
    PARALLELISM_LENGTH_RANGES, PARALLELISM_VALUES,
    COAXIALITY_DIAMETER_RANGES, COAXIALITY_VALUES,
)


# ============================================================
# 核心计算函数
# ============================================================

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


# --- 轴的基本偏差计算 ---

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
        it7 = get_it_value(nominal_size, "IT7")
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


# --- 孔的基本偏差计算 ---

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


# --- 公差查询函数 ---

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
# 尺寸链计算
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
        contribution_val = comp_tol  # 对封闭环公差的贡献 = 该环公差值
        contributions.append({
            "name": comp["name"],
            "ring_type": comp["ring_type"],
            "basic_size": comp["basic_size"],
            "upper_dev": comp["upper_dev"],
            "lower_dev": comp["lower_dev"],
            "tolerance": comp_tol,
            "contribution": contribution_val,
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
# 形位公差查询辅助函数
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
# SVG 生成函数
# ============================================================

def generate_dimension_chain_svg(components):
    """生成尺寸链示意图的SVG - 参考图片结构：总尺寸在上方，分段尺寸在下方"""
    if not components:
        return ""

    # 第一个组成环作为总尺寸
    total_comp = components[0]
    sub_components = components[1:] if len(components) > 1 else []

    # 计算总宽度（基于第一个组成环的尺寸）
    total_size = abs(total_comp["basic_size"])
    if total_size == 0:
        total_size = 100

    # SVG 参数
    svg_width = 800
    svg_height = 250
    margin_left = 80
    margin_right = 50
    margin_top = 40
    margin_bottom = 40

    # 计算绘图区域
    draw_width = svg_width - margin_left - margin_right

    # 上下两层的位置
    upper_y = margin_top + 30  # 总尺寸层
    lower_y = margin_top + 120  # 分段尺寸层

    # 颜色定义
    total_color = "#1565c0"  # 总尺寸 - 蓝色
    sub_colors = ["#388e3c", "#f57c00", "#7b1fa2", "#00796b", "#c62828", "#6a1b9a", "#0277bd", "#2e7d32", "#e65100"]
    closed_color = "#d32f2f"  # 封闭环 - 红色

    # 生成SVG
    svg_parts = [f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">']
    svg_parts.append('<style>')
    svg_parts.append('  text { font-family: Arial, sans-serif; font-size: 13px; }')
    svg_parts.append('  .dim-line { stroke: #333; stroke-width: 1.5; }')
    svg_parts.append('  .dim-text { font-weight: bold; }')
    svg_parts.append('  .total-text { fill: #1565c0; font-size: 15px; }')
    svg_parts.append('  .sub-text { fill: #555; }')
    svg_parts.append('  .closed-text { fill: #d32f2f; font-weight: bold; }')
    svg_parts.append('  .axis-line { stroke: #ccc; stroke-width: 1; }')
    svg_parts.append('</style>')

    # 计算终点X坐标（总尺寸的右端）
    end_x = margin_left + draw_width

    # ========== 上层：总尺寸 ==========
    # 总尺寸界线（左右两根竖线）
    svg_parts.append(f'<line x1="{margin_left}" y1="{upper_y - 15}" x2="{margin_left}" y2="{upper_y + 15}" class="dim-line" stroke="{total_color}"/>')
    svg_parts.append(f'<line x1="{end_x}" y1="{upper_y - 15}" x2="{end_x}" y2="{upper_y + 15}" class="dim-line" stroke="{total_color}"/>')

    # 总尺寸双向箭头（左右都有箭头）
    svg_parts.append(f'<line x1="{margin_left + 10}" y1="{upper_y}" x2="{end_x - 10}" y2="{upper_y}" class="dim-line" stroke="{total_color}"/>')
    # 左箭头
    svg_parts.append(f'<polygon points="{margin_left + 10},{upper_y} {margin_left + 18},{upper_y - 4} {margin_left + 18},{upper_y + 4}" fill="{total_color}"/>')
    # 右箭头
    svg_parts.append(f'<polygon points="{end_x - 10},{upper_y} {end_x - 18},{upper_y - 4} {end_x - 18},{upper_y + 4}" fill="{total_color}"/>')

    # 总尺寸标注（在上方）
    mid_x = (margin_left + end_x) / 2
    svg_parts.append(f'<text x="{mid_x}" y="{upper_y - 8}" text-anchor="middle" class="total-text">{total_comp["name"]} ({total_comp["basic_size"]:.1f})</text>')
    svg_parts.append(f'<text x="{mid_x}" y="{upper_y + 22}" text-anchor="middle" font-size="11" fill="{total_color}">总尺寸 - {total_comp["ring_type"]}</text>')

    # ========== 下层：分段尺寸 ==========
    # 绘制分段尺寸的基准竖线（与总尺寸左对齐）
    svg_parts.append(f'<line x1="{margin_left}" y1="{lower_y - 25}" x2="{margin_left}" y2="{lower_y + 25}" class="dim-line" stroke="#666"/>')

    # 绘制各分段尺寸
    current_x = margin_left
    for i, comp in enumerate(sub_components):
        # 计算尺寸宽度（按比例）
        size_ratio = abs(comp["basic_size"]) / total_size
        segment_width = draw_width * size_ratio

        color = sub_colors[i % len(sub_colors)]
        next_x = current_x + segment_width

        # 尺寸界线（右端竖线）
        svg_parts.append(f'<line x1="{next_x}" y1="{lower_y - 25}" x2="{next_x}" y2="{lower_y + 25}" class="dim-line" stroke="{color}"/>')

        # 尺寸线（带箭头）
        if comp["ring_type"] == "增环":
            # 增环：向右箭头
            svg_parts.append(f'<line x1="{current_x + 5}" y1="{lower_y}" x2="{next_x - 8}" y2="{lower_y}" class="dim-line" stroke="{color}"/>')
            svg_parts.append(f'<polygon points="{next_x - 8},{lower_y} {next_x - 15},{lower_y - 4} {next_x - 15},{lower_y + 4}" fill="{color}"/>')
        else:
            # 减环：向左箭头（从右端指向左端）
            svg_parts.append(f'<line x1="{next_x - 5}" y1="{lower_y}" x2="{current_x + 8}" y2="{lower_y}" class="dim-line" stroke="{color}"/>')
            svg_parts.append(f'<polygon points="{current_x + 8},{lower_y} {current_x + 15},{lower_y - 4} {current_x + 15},{lower_y + 4}" fill="{color}"/>')

        # 尺寸标注
        seg_mid_x = (current_x + next_x) / 2
        svg_parts.append(f'<text x="{seg_mid_x}" y="{lower_y - 10}" text-anchor="middle" class="sub-text" fill="{color}">{comp["name"]} ({comp["basic_size"]:.1f})</text>')
        svg_parts.append(f'<text x="{seg_mid_x}" y="{lower_y + 18}" text-anchor="middle" font-size="10" fill="{color}">{comp["ring_type"]}</text>')

        current_x = next_x

    # 如果只有一个总尺寸，没有分段，显示提示
    if not sub_components:
        svg_parts.append(f'<text x="{margin_left + 20}" y="{lower_y}" font-size="12" fill="#999">（无分段尺寸）</text>')

    # ========== 封闭环 A0 ==========
    # A0 在最左侧，表示间隙
    closed_x = margin_left - 40

    # A0 尺寸界线
    svg_parts.append(f'<line x1="{closed_x}" y1="{lower_y - 20}" x2="{closed_x}" y2="{lower_y + 20}" class="dim-line" stroke="{closed_color}" stroke-width="2"/>')

    # A0 尺寸线（从封闭环到第一个分段）
    svg_parts.append(f'<line x1="{closed_x + 5}" y1="{lower_y}" x2="{margin_left - 8}" y2="{lower_y}" class="dim-line" stroke="{closed_color}"/>')
    svg_parts.append(f'<polygon points="{margin_left - 8},{lower_y} {margin_left - 15},{lower_y - 4} {margin_left - 15},{lower_y + 4}" fill="{closed_color}"/>')

    # A0 标注
    svg_parts.append(f'<text x="{closed_x - 5}" y="{lower_y + 4}" text-anchor="end" class="closed-text">A₀</text>')
    svg_parts.append(f'<text x="{(closed_x + margin_left) / 2}" y="{lower_y - 8}" text-anchor="middle" font-size="10" fill="{closed_color}">封闭环</text>')

    # ========== 连接线和图例 ==========
    # 连接总尺寸和分段尺寸的指引线（虚线）
    svg_parts.append(f'<line x1="{margin_left}" y1="{upper_y + 25}" x2="{margin_left}" y2="{lower_y - 25}" stroke="#ccc" stroke-width="1" stroke-dasharray="3,3"/>')
    svg_parts.append(f'<line x1="{end_x}" y1="{upper_y + 15}" x2="{end_x}" y2="{lower_y - 25}" stroke="#ccc" stroke-width="1" stroke-dasharray="3,3"/>')

    # 图例
    legend_y = svg_height - 15
    svg_parts.append(f'<text x="{svg_width // 2}" y="{legend_y}" text-anchor="middle" font-size="11" fill="#666">📐 尺寸链示意图：{total_comp["name"]}为总尺寸，下方为分段尺寸，A₀为封闭环</text>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_tolerance_zone_svg(hole_info, shaft_info, nominal_size):
    """生成公差带图的SVG - 标准GB/T格式：零线、孔公差带、轴公差带"""
    # 所有偏差值（微米）
    h_es = hole_info["ES"]   # 孔上偏差
    h_ei = hole_info["EI"]   # 孔下偏差
    s_es = shaft_info["ES"]  # 轴上偏差
    s_ei = shaft_info["EI"]  # 轴下偏差

    # 收集所有偏差值确定绘图范围
    all_devs = [h_es, h_ei, s_es, s_ei]
    max_dev = max(all_devs)
    min_dev = min(all_devs)

    # 确保范围合理
    if max_dev == min_dev:
        max_dev = max_dev + 10
        min_dev = min_dev - 10
    range_margin = (max_dev - min_dev) * 0.25
    y_max = max_dev + range_margin
    y_min = min_dev - range_margin

    # SVG 参数
    svg_width = 420
    svg_height = 400
    margin_left = 80
    margin_right = 80
    margin_top = 35
    margin_bottom = 50

    draw_width = svg_width - margin_left - margin_right
    draw_height = svg_height - margin_top - margin_bottom

    # 偏差值到Y坐标的映射（Y轴向下为正，但偏差向上为正）
    def dev_to_y(dev):
        return margin_top + draw_height * (1 - (dev - y_min) / (y_max - y_min))

    zero_y = dev_to_y(0)

    # 颜色
    hole_color = "#d32f2f"    # 孔 - 红色
    shaft_color = "#1565c0"  # 轴 - 蓝色
    zero_color = "#333"      # 零线 - 黑色
    grid_color = "#e0e0e0"   # 网格

    svg = [f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<style>')
    svg.append('  text { font-family: Arial, sans-serif; }')
    svg.append('</style>')

    # ========== 背景网格线 ==========
    # 计算合适的刻度间隔
    dev_range = y_max - y_min
    if dev_range <= 20:
        tick_step = 5
    elif dev_range <= 50:
        tick_step = 10
    elif dev_range <= 100:
        tick_step = 20
    elif dev_range <= 200:
        tick_step = 50
    else:
        tick_step = 100

    tick_start = int(y_min / tick_step) * tick_step
    tick = tick_start
    while tick <= y_max:
        ty = dev_to_y(tick)
        if tick != 0:
            svg.append(f'<line x1="{margin_left}" y1="{ty}" x2="{margin_left + draw_width}" y2="{ty}" stroke="{grid_color}" stroke-width="0.5"/>')
            svg.append(f'<text x="{margin_left - 8}" y="{ty + 4}" text-anchor="end" font-size="11" fill="#666">{tick:.0f}</text>')
        tick += tick_step

    # ========== 零线 ==========
    svg.append(f'<line x1="{margin_left - 5}" y1="{zero_y}" x2="{margin_left + draw_width + 5}" y2="{zero_y}" stroke="{zero_color}" stroke-width="2"/>')
    svg.append(f'<text x="{margin_left - 8}" y="{zero_y + 4}" text-anchor="end" font-size="12" font-weight="bold" fill="{zero_color}">0</text>')
    svg.append(f'<text x="{margin_left + draw_width + 12}" y="{zero_y + 4}" font-size="11" fill="{zero_color}">零线</text>')

    # ========== 孔公差带（红色矩形）==========
    h_top_y = dev_to_y(h_es)
    h_bot_y = dev_to_y(h_ei)
    h_zone_height = abs(h_bot_y - h_top_y)
    if h_zone_height < 2:
        h_zone_height = 2

    # 孔公差带矩形
    hole_rect_x = margin_left + draw_width * 0.2
    hole_rect_w = draw_width * 0.55
    svg.append(f'<rect x="{hole_rect_x}" y="{min(h_top_y, h_bot_y)}" width="{hole_rect_w}" height="{h_zone_height}" fill="{hole_color}" fill-opacity="0.15" stroke="{hole_color}" stroke-width="2"/>')

    # 孔公差带代号标注
    svg.append(f'<text x="{hole_rect_x + hole_rect_w / 2}" y="{min(h_top_y, h_bot_y) - 6}" text-anchor="middle" font-size="14" font-weight="bold" fill="{hole_color}">{hole_info["designation"]}</text>')

    # ES 标注线（孔上偏差）
    svg.append(f'<line x1="{hole_rect_x - 8}" y1="{h_top_y}" x2="{hole_rect_x}" y2="{h_top_y}" stroke="{hole_color}" stroke-width="1.5"/>')
    svg.append(f'<text x="{hole_rect_x - 12}" y="{h_top_y + 4}" text-anchor="end" font-size="11" font-weight="bold" fill="{hole_color}">ES={h_es:+.0f}</text>')

    # EI 标注线（孔下偏差）
    svg.append(f'<line x1="{hole_rect_x - 8}" y1="{h_bot_y}" x2="{hole_rect_x}" y2="{h_bot_y}" stroke="{hole_color}" stroke-width="1.5"/>')
    svg.append(f'<text x="{hole_rect_x - 12}" y="{h_bot_y + 4}" text-anchor="end" font-size="11" font-weight="bold" fill="{hole_color}">EI={h_ei:+.0f}</text>')

    # ========== 轴公差带（蓝色矩形）==========
    s_top_y = dev_to_y(s_es)
    s_bot_y = dev_to_y(s_ei)
    s_zone_height = abs(s_bot_y - s_top_y)
    if s_zone_height < 2:
        s_zone_height = 2

    # 轴公差带矩形
    shaft_rect_x = margin_left + draw_width * 0.25
    shaft_rect_w = draw_width * 0.45
    svg.append(f'<rect x="{shaft_rect_x}" y="{min(s_top_y, s_bot_y)}" width="{shaft_rect_w}" height="{s_zone_height}" fill="{shaft_color}" fill-opacity="0.15" stroke="{shaft_color}" stroke-width="2"/>')

    # 轴公差带代号标注
    svg.append(f'<text x="{shaft_rect_x + shaft_rect_w / 2}" y="{max(s_top_y, s_bot_y) + 16}" text-anchor="middle" font-size="14" font-weight="bold" fill="{shaft_color}">{shaft_info["designation"]}</text>')

    # es 标注线（轴上偏差）
    svg.append(f'<line x1="{shaft_rect_x + shaft_rect_w}" y1="{s_top_y}" x2="{shaft_rect_x + shaft_rect_w + 8}" y2="{s_top_y}" stroke="{shaft_color}" stroke-width="1.5"/>')
    svg.append(f'<text x="{shaft_rect_x + shaft_rect_w + 12}" y="{s_top_y + 4}" text-anchor="start" font-size="11" font-weight="bold" fill="{shaft_color}">es={s_es:+.0f}</text>')

    # ei 标注线（轴下偏差）
    svg.append(f'<line x1="{shaft_rect_x + shaft_rect_w}" y1="{s_bot_y}" x2="{shaft_rect_x + shaft_rect_w + 8}" y2="{s_bot_y}" stroke="{shaft_color}" stroke-width="1.5"/>')
    svg.append(f'<text x="{shaft_rect_x + shaft_rect_w + 12}" y="{s_bot_y + 4}" text-anchor="start" font-size="11" font-weight="bold" fill="{shaft_color}">ei={s_ei:+.0f}</text>')

    # ========== 配合区域标注 ==========
    # 判断配合类型并标注间隙/过盈区域
    if h_ei >= s_es:
        # 间隙配合：标注最大间隙和最小间隙
        x_max_cl_y = dev_to_y(h_es)
        x_min_cl_y = dev_to_y(s_ei)
        mid_cl_y = (x_max_cl_y + x_min_cl_y) / 2
        arrow_x = margin_left + draw_width * 0.5
        # 最大间隙标注
        svg.append(f'<line x1="{arrow_x}" y1="{x_max_cl_y}" x2="{arrow_x}" y2="{x_min_cl_y}" stroke="#e65100" stroke-width="1" stroke-dasharray="4,3"/>')
        svg.append(f'<polygon points="{arrow_x},{x_max_cl_y} {arrow_x-3},{x_max_cl_y+6} {arrow_x+3},{x_max_cl_y+6}" fill="#e65100"/>')
        svg.append(f'<polygon points="{arrow_x},{x_min_cl_y} {arrow_x-3},{x_min_cl_y-6} {arrow_x+3},{x_min_cl_y-6}" fill="#e65100"/>')
        max_cl_val = h_es - s_ei
        svg.append(f'<text x="{arrow_x + 6}" y="{mid_cl_y + 4}" font-size="10" fill="#e65100">Xmax={max_cl_val:.0f}μm</text>')
    elif h_es <= s_ei:
        # 过盈配合
        y_max_int_y = dev_to_y(s_ei)
        y_min_int_y = dev_to_y(h_es)
        mid_int_y = (y_max_int_y + y_min_int_y) / 2
        arrow_x = margin_left + draw_width * 0.5
        svg.append(f'<line x1="{arrow_x}" y1="{y_max_int_y}" x2="{arrow_x}" y2="{y_min_int_y}" stroke="#e65100" stroke-width="1" stroke-dasharray="4,3"/>')
        svg.append(f'<polygon points="{arrow_x},{y_max_int_y} {arrow_x-3},{y_max_int_y+6} {arrow_x+3},{y_max_int_y+6}" fill="#e65100"/>')
        svg.append(f'<polygon points="{arrow_x},{y_min_int_y} {arrow_x-3},{y_min_int_y-6} {arrow_x+3},{y_min_int_y-6}" fill="#e65100"/>')
        max_int_val = s_ei - h_es
        svg.append(f'<text x="{arrow_x + 6}" y="{mid_int_y + 4}" font-size="10" fill="#e65100">Ymax={max_int_val:.0f}μm</text>')

    # ========== 底部信息 ==========
    svg.append(f'<text x="{svg_width / 2}" y="{svg_height - 15}" text-anchor="middle" font-size="12" fill="#333">公称尺寸 φ{nominal_size} mm | 单位: μm</text>')
    svg.append(f'<text x="{svg_width / 2}" y="{svg_height - 2}" text-anchor="middle" font-size="10" fill="#999">数据来源: GB/T 1800.1-2020</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def generate_gdandt_annotation_svg(item_name, tol_value_um, grade, param_value):
    """生成形位公差标注示例的SVG - 标准GB/T 1182格式

    包含: 形位公差框格(符号+公差值+基准)、指引线、箭头、基准符号、零件简图
    """
    # 形位公差符号定义 (Unicode/自定义SVG路径)
    # needs_diameter: 是否需要在公差值前加直径符号φ（同轴度、对称度、位置度需要）
    symbol_map = {
        "圆度": {"symbol": "○", "svg_path": None, "has_datum": False, "needs_diameter": False,
                 "desc": "被测要素为圆柱面/球面的横截面", "arrow_to": "轮廓线"},
        "圆柱度": {"symbol": "⌭", "svg_path": None, "has_datum": False, "needs_diameter": False,
                   "desc": "被测要素为圆柱面", "arrow_to": "尺寸线"},
        "直线度": {"symbol": "—", "svg_path": None, "has_datum": False, "needs_diameter": False,
                   "desc": "被测要素为轴线或表面素线", "arrow_to": "尺寸线"},
        "平面度": {"symbol": "▱", "svg_path": None, "has_datum": False, "needs_diameter": False,
                   "desc": "被测要素为平面表面", "arrow_to": "轮廓线"},
        "平行度": {"symbol": "∥", "svg_path": None, "has_datum": True, "needs_diameter": False,
                   "desc": "被测要素相对于基准平行", "arrow_to": "尺寸线"},
        "垂直度": {"symbol": "⊥", "svg_path": None, "has_datum": True, "needs_diameter": False,
                   "desc": "被测要素相对于基准垂直", "arrow_to": "轮廓线"},
        "同轴度": {"symbol": "◎", "svg_path": None, "has_datum": True, "needs_diameter": True,
                   "desc": "被测轴线相对于基准轴线同轴", "arrow_to": "尺寸线"},
        "对称度": {"symbol": "⌢", "svg_path": None, "has_datum": True, "needs_diameter": True,
                   "desc": "被测中心面相对于基准中心面对称", "arrow_to": "尺寸线"},
        "圆跳动": {"symbol": "↗", "svg_path": None, "has_datum": True, "needs_diameter": False,
                   "desc": "被测要素相对于基准的圆跳动", "arrow_to": "轮廓线"},
        "全跳动": {"symbol": "⇗", "svg_path": None, "has_datum": True, "needs_diameter": False,
                   "desc": "被测要素相对于基准的全跳动", "arrow_to": "轮廓线"},
        "位置度": {"symbol": "⌖", "svg_path": None, "has_datum": True, "needs_diameter": True,
                   "desc": "被测要素相对于基准的位置", "arrow_to": "尺寸线"},
        "倾斜度": {"symbol": "∠", "svg_path": None, "has_datum": True, "needs_diameter": False,
                   "desc": "被测要素相对于基准倾斜", "arrow_to": "轮廓线"},
    }

    info = symbol_map.get(item_name, {"symbol": "?", "svg_path": None, "has_datum": True, "needs_diameter": False,
                                       "desc": "被测要素", "arrow_to": "轮廓线"})

    # 将公差值从微米转换为毫米显示，并根据需要添加直径符号φ
    if tol_value_um >= 1000:
        tol_mm_str = f"{tol_value_um / 1000:.1f}"
    else:
        tol_mm_str = f"{tol_value_um / 1000:.3f}"

    # 同轴度、对称度、位置度需要加直径符号φ
    if info.get("needs_diameter", False):
        tol_display = f"φ{tol_mm_str}"
    else:
        tol_display = tol_mm_str

    has_datum = info["has_datum"]

    # SVG 参数
    svg_width = 520
    svg_height = 250

    svg = [f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<style>')
    svg.append('  text { font-family: Arial, sans-serif; }')
    svg.append('  .thick { stroke: #333; stroke-width: 2.5; }')
    svg.append('  .thin { stroke: #333; stroke-width: 1; }')
    svg.append('  .center { stroke: #333; stroke-width: 0.8; stroke-dasharray: 12,3,3,3; }')
    svg.append('  .frame-text { font-size: 14px; font-weight: bold; fill: #1565c0; }')
    svg.append('  .label { font-size: 11px; fill: #555; }')
    svg.append('  .datum-text { font-size: 13px; font-weight: bold; fill: #d32f2f; }')
    svg.append('  .desc-text { font-size: 10px; fill: #888; }')
    svg.append('</style>')

    # ========== 零件简图（右侧）==========
    part_x = 300
    part_y = 50
    part_w = 180
    part_h = 80

    # 零件外形 - 分为两段：左段(被测要素) + 右段(基准要素)
    # 左段：被测要素
    left_part_w = part_w * 0.45
    svg.append(f'<rect x="{part_x}" y="{part_y}" width="{left_part_w}" height="{part_h}" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="2"/>')

    # 右段：基准要素（稍大一些，表示基准轴颈）
    right_part_x = part_x + left_part_w
    right_part_w = part_w * 0.55
    svg.append(f'<rect x="{right_part_x}" y="{part_y - 5}" width="{right_part_w}" height="{part_h + 10}" fill="#ffebee" stroke="#333" stroke-width="2" rx="2"/>')

    # 中心线
    svg.append(f'<line x1="{part_x - 20}" y1="{part_y + part_h // 2}" x2="{part_x + part_w + 20}" y2="{part_y + part_h // 2}" class="center"/>')

    # 被测要素指示箭头（指向左段零件）
    arrow_target_y = part_y + part_h // 2
    if info["arrow_to"] == "轮廓线":
        # 箭头指向轮廓线
        svg.append(f'<line x1="{part_x + 30}" y1="{part_y - 5}" x2="{part_x + 30}" y2="{part_y}" stroke="#1565c0" stroke-width="1.5"/>')
        svg.append(f'<polygon points="{part_x + 30},{part_y} {part_x + 26},{part_y - 6} {part_x + 34},{part_y - 6}" fill="#1565c0"/>')
        leader_end_y = part_y - 5
    else:
        # 箭头指向尺寸线
        svg.append(f'<line x1="{part_x + 30}" y1="{arrow_target_y - 15}" x2="{part_x + 30}" y2="{arrow_target_y - 8}" stroke="#1565c0" stroke-width="1.5"/>')
        svg.append(f'<polygon points="{part_x + 30},{arrow_target_y - 8} {part_x + 26},{arrow_target_y - 14} {part_x + 34},{arrow_target_y - 14}" fill="#1565c0"/>')
        leader_end_y = arrow_target_y - 15

    # 被测要素标注
    svg.append(f'<text x="{part_x + left_part_w // 2}" y="{part_y + part_h + 15}" text-anchor="middle" class="desc-text">被测要素</text>')

    # ========== 形位公差框格（左侧）==========
    frame_x = 30
    frame_y = 30
    cell_w = 50
    cell_h = 28

    # 框格背景
    if has_datum:
        total_frame_w = cell_w * 3
    else:
        total_frame_w = cell_w * 2

    svg.append(f'<rect x="{frame_x}" y="{frame_y}" width="{total_frame_w}" height="{cell_h}" fill="white" stroke="#333" stroke-width="2"/>')

    # 分隔线
    svg.append(f'<line x1="{frame_x + cell_w}" y1="{frame_y}" x2="{frame_x + cell_w}" y2="{frame_y + cell_h}" stroke="#333" stroke-width="1"/>')
    svg.append(f'<line x1="{frame_x + cell_w * 2}" y1="{frame_y}" x2="{frame_x + cell_w * 2}" y2="{frame_y + cell_h}" stroke="#333" stroke-width="1"/>')

    # 第一格：形位公差符号（放大显示）
    symbol_cx = frame_x + cell_w // 2
    symbol_cy = frame_y + cell_h // 2 + 1
    svg.append(f'<text x="{symbol_cx}" y="{symbol_cy + 6}" text-anchor="middle" font-size="24" font-weight="bold" fill="#1565c0">{info["symbol"]}</text>')

    # 第二格：公差值（同轴度、对称度、位置度需加直径符号φ）
    val_cx = frame_x + cell_w + cell_w // 2
    svg.append(f'<text x="{val_cx}" y="{symbol_cy + 5}" text-anchor="middle" class="frame-text">{tol_display}</text>')

    # 第三格：基准字母（如果有）
    if has_datum:
        datum_cx = frame_x + cell_w * 2 + cell_w // 2
        svg.append(f'<text x="{datum_cx}" y="{symbol_cy + 5}" text-anchor="middle" class="datum-text">A</text>')

    # ========== 指引线（从框格到零件）==========
    # 水平段
    guide_start_x = frame_x + total_frame_w
    guide_end_x = part_x + 30
    guide_y = frame_y + cell_h // 2

    svg.append(f'<line x1="{guide_start_x}" y1="{guide_y}" x2="{guide_end_x}" y2="{guide_y}" stroke="#1565c0" stroke-width="1.2"/>')

    # 垂直段（从水平指引线到零件）
    svg.append(f'<line x1="{guide_end_x}" y1="{guide_y}" x2="{guide_end_x}" y2="{leader_end_y}" stroke="#1565c0" stroke-width="1.2"/>')

    # ========== 基准符号（如果有）==========
    if has_datum:
        # 基准符号标注在基准要素上（右段零件）
        datum_x = right_part_x + right_part_w // 2
        datum_y = part_y - 5  # 基准要素顶部

        # 基准指引线（从零件顶部向上）
        svg.append(f'<line x1="{datum_x}" y1="{datum_y}" x2="{datum_x}" y2="{datum_y - 25}" stroke="#d32f2f" stroke-width="1.2"/>')

        # 基准三角形（倒三角形，指向基准要素）
        tri_top_y = datum_y - 25
        svg.append(f'<polygon points="{datum_x - 8},{tri_top_y} {datum_x + 8},{tri_top_y} {datum_x},{tri_top_y + 10}" fill="#d32f2f" stroke="#d32f2f" stroke-width="1"/>')

        # 基准字母框（在三角形上方）
        box_y = tri_top_y - 22
        svg.append(f'<rect x="{datum_x - 12}" y="{box_y}" width="24" height="18" fill="white" stroke="#d32f2f" stroke-width="1.5"/>')
        svg.append(f'<text x="{datum_x}" y="{box_y + 14}" text-anchor="middle" font-size="13" font-weight="bold" fill="#d32f2f">A</text>')

        # 基准要素标注
        svg.append(f'<text x="{datum_x}" y="{part_y + part_h + 15}" text-anchor="middle" class="desc-text" fill="#d32f2f">基准要素A</text>')

    # ========== 标注说明文字 ==========
    desc_y = svg_height - 60

    # 公差项目名称
    svg.append(f'<text x="{frame_x}" y="{frame_y + cell_h + 20}" font-size="13" font-weight="bold" fill="#333">{item_name} (等级{grade})</text>')

    # 标注说明
    svg.append(f'<text x="{frame_x}" y="{desc_y}" class="label">📌 {info["desc"]}</text>')
    svg.append(f'<text x="{frame_x}" y="{desc_y + 16}" class="label">📌 指引线箭头指向被测要素({info["arrow_to"]})</text>')
    if has_datum:
        svg.append(f'<text x="{frame_x}" y="{desc_y + 32}" class="label">📌 基准A标注在基准要素上（红色区域）</text>')

    # 公差值说明
    if info.get("needs_diameter", False):
        svg.append(f'<text x="{frame_x + total_frame_w + 10}" y="{frame_y + cell_h + 20}" class="label">公差值: φ{tol_mm_str} mm (直径符号φ表示公差带为圆柱面)</text>')
    else:
        svg.append(f'<text x="{frame_x + total_frame_w + 10}" y="{frame_y + cell_h + 20}" class="label">公差值: {tol_mm_str} mm ({tol_value_um} μm)</text>')

    # 标准参考
    svg.append(f'<text x="{svg_width // 2}" y="{svg_height - 8}" text-anchor="middle" class="desc-text">标注依据: GB/T 1182-2018 (ISO 1101)</text>')

    svg.append('</svg>')
    return '\n'.join(svg)
