# -*- coding: utf-8 -*-
"""
形位公差推荐数据 (GB/T 1184-1996)
包含：各零件类型功能部位的形位公差推荐
"""

# --- 3.6 形位公差推荐 ---
GEOMETRIC_TOLERANCE_RECOMMENDATIONS = {
    "轴类": {
        "支撑轴颈（滚动轴承配合面）": [
            {
                "item": "圆度",
                "grade_range": (5, 7),
                "reason": "轴颈圆度直接影响轴承运转精度和噪声。圆度误差过大导致轴承振动和磨损加剧。",
                "standard_ref": "GB/T 1184",
                "application": "电动机轴、主轴、传动轴的轴承配合段"
            },
            {
                "item": "圆柱度",
                "grade_range": (5, 7),
                "reason": "圆柱度误差影响轴承配合均匀性，可能导致局部应力集中和早期失效。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度配合使用，综合控制轴颈形状"
            },
            {
                "item": "径向圆跳动",
                "grade_range": (5, 7),
                "reason": "综合反映轴颈的形状误差和同轴度误差，是验收轴类零件的重要指标。",
                "standard_ref": "GB/T 1184",
                "application": "测量时将轴旋转一周，百分表读数差即为跳动量"
            },
            {
                "item": "同轴度",
                "grade_range": (5, 8),
                "reason": "多阶梯轴各轴颈的同轴度影响轴承装配和转子动平衡。",
                "standard_ref": "GB/T 1184",
                "application": "阶梯轴、齿轮轴、电机轴等"
            },
        ],
        "轴肩过渡处": [
            {
                "item": "垂直度",
                "grade_range": (6, 8),
                "reason": "轴肩端面垂直度影响滚动轴承、齿轮等零件的轴向定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "轴承定位肩、齿轮挡边、联轴器定位面"
            },
            {
                "item": "圆跳动（端面）",
                "grade_range": (6, 8),
                "reason": "轴肩端面跳动影响零件的轴向位置精度和受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "测量轴肩对轴线的跳动"
            },
        ],
        "键槽配合面": [
            {
                "item": "对称度",
                "grade_range": (7, 9),
                "reason": "键槽对称度误差导致键受力不均，产生附加弯矩，加速键和键槽磨损。",
                "standard_ref": "GB/T 1184",
                "application": "普通平键槽、半圆键槽、楔键槽"
            },
            {
                "item": "平行度",
                "grade_range": (7, 9),
                "reason": "键槽侧面对轴线的平行度影响键的装配和传动平稳性。",
                "standard_ref": "GB/T 1184",
                "application": "与对称度同时控制"
            },
            {
                "item": "位置度",
                "grade_range": (8, 10),
                "reason": "花键配合的花键轴，各键中心对基准轴线的位置度误差影响花键装配。",
                "standard_ref": "GB/T 1184",
                "application": "矩形花键、渐开线花键"
            },
        ],
        "外圆表面（非轴承面）": [
            {
                "item": "圆度",
                "grade_range": (6, 9),
                "reason": "非轴承配合面的圆度误差影响外观和装配。",
                "standard_ref": "GB/T 1184",
                "application": "装饰面、填料函处"
            },
            {
                "item": "圆柱度",
                "grade_range": (6, 9),
                "reason": "圆柱度误差影响非配合段与其他零件的相对位置。",
                "standard_ref": "GB/T 1184",
                "application": "一般传动轴的非配合段"
            },
        ],
        "螺纹部分": [
            {
                "item": "同轴度",
                "grade_range": (6, 8),
                "reason": "螺纹轴线对基准轴颈的同轴度影响螺纹旋合质量和传动精度。",
                "standard_ref": "GB/T 1184",
                "application": "丝杠、蜗杆、传动螺纹"
            },
            {
                "item": "圆跳动（径向）",
                "grade_range": (6, 9),
                "reason": "螺纹牙侧面的跳动影响螺纹配合精度。",
                "standard_ref": "GB/T 1184",
                "application": "测量螺纹牙侧面对轴线的跳动"
            },
        ],
        "定位台阶面": [
            {
                "item": "垂直度",
                "grade_range": (6, 8),
                "reason": "定位台阶面对轴线的垂直度影响被固定零件的定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "轴承挡肩、齿轮定位台阶"
            },
            {
                "item": "圆跳动（端面）",
                "grade_range": (6, 8),
                "reason": "定位端面跳动影响被固定件的受力均匀性和定位可靠性。",
                "standard_ref": "GB/T 1184",
                "application": "轴向定位面"
            },
        ],
    },
    "孔类": {
        "轴承孔（箱体/座孔）": [
            {
                "item": "圆度",
                "grade_range": (5, 7),
                "reason": "轴承孔圆度误差直接影响轴承外圈变形和运转精度，加速轴承损坏。",
                "standard_ref": "GB/T 1184",
                "application": "减速器箱体孔、电机端盖孔、泵体轴承孔"
            },
            {
                "item": "圆柱度",
                "grade_range": (5, 7),
                "reason": "圆柱度误差导致轴承外圈受力不均，影响轴承寿命。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度配合使用"
            },
            {
                "item": "同轴度",
                "grade_range": (5, 7),
                "reason": "箱体上同轴孔的同轴度误差严重影响轴系装配和运转精度。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱体两侧轴承孔、电机机体与端盖轴承孔"
            },
            {
                "item": "径向圆跳动",
                "grade_range": (5, 7),
                "reason": "综合控制轴承孔的形状和位置误差，是箱体检测的关键指标。",
                "standard_ref": "GB/T 1184",
                "application": "箱体轴承孔出厂检验"
            },
        ],
        "定位销孔": [
            {
                "item": "位置度",
                "grade_range": (6, 8),
                "reason": "销孔位置度误差直接影响零件定位精度，影响装配互换性。",
                "standard_ref": "GB/T 1184",
                "application": "箱体剖分面定位销孔、夹具定位孔"
            },
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "销孔圆度误差影响销与孔的配合精度。",
                "standard_ref": "GB/T 1184",
                "application": "圆柱销定位孔"
            },
            {
                "item": "垂直度（相对基准面）",
                "grade_range": (7, 9),
                "reason": "销孔轴线对基准面的垂直度影响定位销的插入和定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "精密机床夹具销孔"
            },
        ],
        "螺纹孔": [
            {
                "item": "位置度",
                "grade_range": (7, 10),
                "reason": "螺纹孔位置度误差影响螺栓装配和连接强度。",
                "standard_ref": "GB/T 1184",
                "application": "减速器箱盖螺孔、支架安装孔"
            },
            {
                "item": "垂直度（相对被连接面）",
                "grade_range": (7, 10),
                "reason": "螺纹孔轴线对端面的垂直度影响螺栓杆的受力和装配质量。",
                "standard_ref": "GB/T 1184",
                "application": "法兰端面螺孔、箱体安装面螺孔"
            },
            {
                "item": "同轴度（盲孔族）",
                "grade_range": (8, 10),
                "reason": "多螺纹孔对同一基准的同轴度影响螺栓均匀受力。",
                "standard_ref": "GB/T 1184",
                "application": "均匀分布的法兰螺孔组"
            },
        ],
        "齿轮安装孔": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "齿轮孔圆度误差影响齿轮与轴的配合质量和平稳运转。",
                "standard_ref": "GB/T 1184",
                "application": "减速器齿轮轮毂孔"
            },
            {
                "item": "同轴度（相对基准孔）",
                "grade_range": (6, 8),
                "reason": "齿轮安装孔对轴承孔的同轴度影响齿轮啮合精度和噪声。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱体上齿轮安装孔"
            },
            {
                "item": "端面圆跳动",
                "grade_range": (7, 9),
                "reason": "齿轮定位端面跳动影响齿轮轴向定位精度和受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "齿轮定位肩面"
            },
        ],
        "液压/气动通道孔": [
            {
                "item": "圆度",
                "grade_range": (7, 10),
                "reason": "通道孔圆度影响密封件寿命和流体流通效率。",
                "standard_ref": "GB/T 1184",
                "application": "液压阀体油孔、气缸筒壁孔"
            },
            {
                "item": "位置度",
                "grade_range": (8, 10),
                "reason": "通道孔位置度误差影响管路连接和流体分配。",
                "standard_ref": "GB/T 1184",
                "application": "多通道交叉孔系"
            },
            {
                "item": "垂直度",
                "grade_range": (8, 10),
                "reason": "密封面孔的垂直度影响密封效果。",
                "standard_ref": "GB/T 1184",
                "application": "液压阀块安装面"
            },
        ],
        "深孔（枪钻/镗削）": [
            {
                "item": "圆度",
                "grade_range": (6, 9),
                "reason": "深孔圆度误差反映镗削稳定性和刀具状态。",
                "standard_ref": "GB/T 1184",
                "application": "液压缸筒、深孔套筒"
            },
            {
                "item": "直线度",
                "grade_range": (6, 9),
                "reason": "深孔直线度误差影响活塞杆/心轴通过性和密封寿命。",
                "standard_ref": "GB/T 1184",
                "application": "液压缸筒、炮管、模具导套"
            },
        ],
    },
    "齿轮类": {
        "齿坯基准孔/轴": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "齿坯基准孔/轴圆度直接影响齿轮与轴的配合质量和啮合精度。",
                "standard_ref": "GB/T 1184",
                "application": "齿轮轮毂孔、齿轮轴颈"
            },
            {
                "item": "圆柱度",
                "grade_range": (6, 8),
                "reason": "圆柱度误差影响配合面接触均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度配合使用"
            },
            {
                "item": "同轴度（相对基准）",
                "grade_range": (6, 8),
                "reason": "齿圈相对基准孔/轴的同轴度误差直接影响齿轮啮合质量。",
                "standard_ref": "GB/T 1184",
                "application": "齿轮安装基准面对齿圈跳动"
            },
            {
                "item": "径向圆跳动",
                "grade_range": (6, 8),
                "reason": "齿圈径向跳动是评价齿轮精度的重要指标，影响传动平稳性。",
                "standard_ref": "GB/T 1184",
                "application": "齿轮齿圈对基准孔的跳动"
            },
            {
                "item": "端面圆跳动",
                "grade_range": (6, 8),
                "reason": "齿轮基准端面跳动影响齿轮轴向定位和受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "锥齿轮法兰端面、圆柱齿轮轴肩"
            },
        ],
        "齿轮定位键槽": [
            {
                "item": "对称度",
                "grade_range": (7, 9),
                "reason": "键槽对称度误差导致键受力不均，产生附加弯矩，加速键和键槽磨损。",
                "standard_ref": "GB/T 1184",
                "application": "齿轮、平键连接"
            },
            {
                "item": "平行度",
                "grade_range": (7, 9),
                "reason": "键槽侧面对轴线的平行度影响键的装配和传动平稳性。",
                "standard_ref": "GB/T 1184",
                "application": "与对称度同时控制"
            },
        ],
        "齿坯外圆/止口": [
            {
                "item": "圆度",
                "grade_range": (7, 9),
                "reason": "齿坯外圆/止口圆度影响齿轮在装配中的定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "齿轮外圆、法兰止口"
            },
            {
                "item": "同轴度",
                "grade_range": (7, 9),
                "reason": "齿坯外圆对基准孔的同轴度影响齿轮定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "齿坯外圆对基准孔"
            },
        ],
    },
    "箱体类": {
        "轴承孔系": [
            {
                "item": "同轴度（孔系间）",
                "grade_range": (5, 7),
                "reason": "箱体轴承孔系同轴度误差是轴系装配误差的主要来源，直接影响齿轮啮合精度和噪声。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱体主从动轴轴承孔"
            },
            {
                "item": "平行度（孔系轴线间）",
                "grade_range": (5, 7),
                "reason": "轴承孔轴线平行度误差导致齿轮轴线不平行，影响齿面接触和传动精度。",
                "standard_ref": "GB/T 1184",
                "application": "斜齿轮、蜗轮蜗杆箱体"
            },
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "轴承孔圆度误差影响轴承外圈配合均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "轴承安装孔"
            },
            {
                "item": "圆柱度",
                "grade_range": (6, 8),
                "reason": "圆柱度误差与圆度配合控制轴承孔形状精度。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度同时控制"
            },
            {
                "item": "位置度（孔间距）",
                "grade_range": (6, 8),
                "reason": "孔间距位置度误差影响齿轮中心距和啮合精度。",
                "standard_ref": "GB/T 1184",
                "application": "孔系中心距"
            },
        ],
        "结合面（剖分面/安装面）": [
            {
                "item": "平面度",
                "grade_range": (6, 8),
                "reason": "箱体结合面平面度误差直接影响密封性能，漏油是最常见的故障之一。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱盖与箱座结合面"
            },
            {
                "item": "平行度（结合面对轴承孔轴线）",
                "grade_range": (7, 9),
                "reason": "结合面对轴承孔轴线的平行度影响轴承孔中心高度精度。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱体底面"
            },
            {
                "item": "垂直度（侧面对底面）",
                "grade_range": (7, 9),
                "reason": "箱体侧面垂直度影响整机装配和外观。",
                "standard_ref": "GB/T 1184",
                "application": "箱体安装侧面"
            },
        ],
        "定位销孔": [
            {
                "item": "位置度",
                "grade_range": (6, 8),
                "reason": "剖分箱体销孔位置度决定剖分面定位精度，影响轴承孔同轴度。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱盖与箱座定位销孔"
            },
            {
                "item": "同轴度（相对轴承孔）",
                "grade_range": (7, 9),
                "reason": "定位销孔对轴承孔的同轴度影响定位销的装配。",
                "standard_ref": "GB/T 1184",
                "application": "精密机床箱体"
            },
        ],
        "安装基面": [
            {
                "item": "平面度",
                "grade_range": (7, 10),
                "reason": "安装基面平面度影响设备安装水平和受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "减速机底面、电机安装面"
            },
            {
                "item": "平行度（相对轴承孔轴线）",
                "grade_range": (7, 10),
                "reason": "安装基面对轴承孔轴线的平行度影响设备安装后的轴线高度。",
                "standard_ref": "GB/T 1184",
                "application": "减速机底面"
            },
        ],
        "油孔/油尺孔": [
            {
                "item": "位置度",
                "grade_range": (9, 11),
                "reason": "油孔位置影响油路布置和加油便利性。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱体油孔"
            },
            {
                "item": "垂直度",
                "grade_range": (9, 11),
                "reason": "油尺孔垂直度影响油尺插入和油位测量准确性。",
                "standard_ref": "GB/T 1184",
                "application": "油尺安装孔"
            },
        ],
    },
    "法兰类": {
        "密封面（端面密封）": [
            {
                "item": "平面度",
                "grade_range": (5, 8),
                "reason": "密封面平面度是保证密封效果的首要条件，平面度误差直接导致泄漏。",
                "standard_ref": "GB/T 1184",
                "application": "管道法兰密封面、阀门端盖、液压阀块安装面"
            },
            {
                "item": "垂直度（密封面对轴线）",
                "grade_range": (6, 8),
                "reason": "密封面对轴线垂直度影响密封垫片的压缩均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "液压缸端盖、法兰"
            },
            {
                "item": "圆跳动（密封面）",
                "grade_range": (6, 8),
                "reason": "密封面径向跳动反映密封面的对称性和均匀受压程度。",
                "standard_ref": "GB/T 1184",
                "application": "回转密封面"
            },
        ],
        "定位止口/凸台": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "定位止口圆度决定法兰定位精度，影响同轴装配。",
                "standard_ref": "GB/T 1184",
                "application": "法兰定位止口、阀体安装凸台"
            },
            {
                "item": "同轴度（止口相对密封面）",
                "grade_range": (6, 8),
                "reason": "止口对密封面的同轴度误差导致密封不均匀，影响密封效果。",
                "standard_ref": "GB/T 1184",
                "application": "法兰止口与密封面"
            },
            {
                "item": "垂直度（止口对端面）",
                "grade_range": (6, 8),
                "reason": "止口轴线对端面的垂直度影响法兰装配定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "法兰止口"
            },
        ],
        "连接螺栓孔": [
            {
                "item": "位置度",
                "grade_range": (7, 10),
                "reason": "螺栓孔位置度误差影响螺栓装配和连接强度，严重时无法装配。",
                "standard_ref": "GB/T 1184",
                "application": "法兰连接孔、管板孔"
            },
            {
                "item": "垂直度（螺栓孔对法兰面）",
                "grade_range": (8, 10),
                "reason": "螺栓孔轴线对法兰面的垂直度影响螺栓杆受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "压力容器法兰"
            },
            {
                "item": "同轴度（孔组对基准）",
                "grade_range": (8, 10),
                "reason": "均匀分布的螺栓孔组对公共基准的同轴度影响装配互换性。",
                "standard_ref": "GB/T 1184",
                "application": "标准法兰盘"
            },
        ],
        "密封环槽": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "密封环槽圆度误差影响密封圈压缩量均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "O形圈沟槽、静密封面"
            },
            {
                "item": "同轴度（环槽相对基准）",
                "grade_range": (6, 8),
                "reason": "环槽对基准的同轴度影响密封件受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "轴套密封槽"
            },
        ],
    },
    "端盖/箱盖类": {
        "密封配合面": [
            {
                "item": "平面度",
                "grade_range": (6, 8),
                "reason": "端盖配合面平面度直接影响密封效果，是最关键的形位公差项目。",
                "standard_ref": "GB/T 1184",
                "application": "减速机箱盖、电机端盖、阀门端盖"
            },
            {
                "item": "垂直度（配合面对轴线）",
                "grade_range": (6, 8),
                "reason": "端盖配合面对轴线的垂直度影响密封件压缩均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "迷宫密封端盖"
            },
        ],
        "轴承孔（如为轴承座）": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "端盖轴承孔圆度误差影响轴承外圈配合和运转精度。",
                "standard_ref": "GB/T 1184",
                "application": "轴承压盖、轴承座端盖"
            },
            {
                "item": "同轴度（相对配合止口）",
                "grade_range": (6, 8),
                "reason": "端盖轴承孔对止口的同轴度影响轴的装配和运转。",
                "standard_ref": "GB/T 1184",
                "application": "轴承压盖"
            },
            {
                "item": "圆柱度",
                "grade_range": (6, 8),
                "reason": "圆柱度误差与圆度配合控制孔形状精度。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度同时控制"
            },
        ],
        "定位止口": [
            {
                "item": "圆度",
                "grade_range": (7, 9),
                "reason": "定位止口圆度决定端盖定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "端盖定位止口"
            },
            {
                "item": "同轴度（相对配合面）",
                "grade_range": (7, 9),
                "reason": "止口对配合面的同轴度影响密封效果。",
                "standard_ref": "GB/T 1184",
                "application": "端盖"
            },
        ],
        "螺钉孔": [
            {
                "item": "位置度",
                "grade_range": (8, 10),
                "reason": "螺钉孔位置度误差影响螺钉装配和连接强度。",
                "standard_ref": "GB/T 1184",
                "application": "端盖固定螺钉孔"
            },
            {
                "item": "垂直度（相对配合面）",
                "grade_range": (8, 10),
                "reason": "螺钉孔轴线对配合面的垂直度影响螺钉受力。",
                "standard_ref": "GB/T 1184",
                "application": "盖板螺钉孔"
            },
        ],
    },
    "导轨类": {
        "滑动导轨面": [
            {
                "item": "直线度（纵向）",
                "grade_range": (5, 8),
                "reason": "导轨纵向直线度误差直接影响运动精度，是机床导轨最基本的形位要求。",
                "standard_ref": "GB/T 1184",
                "application": "车床床身导轨、铣床工作台导轨"
            },
            {
                "item": "平面度（横向）",
                "grade_range": (5, 8),
                "reason": "导轨横向平面度影响运动副接触均匀性和导轨受力分布。",
                "standard_ref": "GB/T 1184",
                "application": "床身导轨顶面"
            },
            {
                "item": "平行度（两导轨间）",
                "grade_range": (5, 8),
                "reason": "双矩形导轨平行度误差影响运动直线性和定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "双V导轨、双矩形导轨"
            },
            {
                "item": "垂直度（导轨对基准面）",
                "grade_range": (6, 8),
                "reason": "导轨对基准安装面的垂直度影响设备安装精度。",
                "standard_ref": "GB/T 1184",
                "application": "床身导轨对底面"
            },
        ],
        "燕尾导轨": [
            {
                "item": "直线度",
                "grade_range": (6, 8),
                "reason": "燕尾导轨直线度误差影响滑动精度。",
                "standard_ref": "GB/T 1184",
                "application": "车床溜板箱燕尾导轨"
            },
            {
                "item": "平行度（导轨宽度方向）",
                "grade_range": (6, 8),
                "reason": "燕尾导轨平行度影响塞尺调整精度。",
                "standard_ref": "GB/T 1184",
                "application": "燕尾配合面"
            },
            {
                "item": "角度（燕尾角）",
                "grade_range": (8, 10),
                "reason": "燕尾角误差影响配合间隙调整范围。",
                "standard_ref": "GB/T 1184",
                "application": "燕尾导轨"
            },
        ],
        "导轨安装基准面": [
            {
                "item": "平面度",
                "grade_range": (7, 9),
                "reason": "导轨安装基准面平面度影响导轨安装水平度和受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "床身与地基接触面"
            },
            {
                "item": "平行度（安装面对导轨面）",
                "grade_range": (7, 9),
                "reason": "安装面对导轨面的平行度影响导轨直线度。",
                "standard_ref": "GB/T 1184",
                "application": "安装基准"
            },
        ],
        "定位键槽（T型槽）": [
            {
                "item": "直线度",
                "grade_range": (7, 9),
                "reason": "T型槽直线度影响定位键的装配和定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "机床工作台T型槽"
            },
            {
                "item": "位置度",
                "grade_range": (7, 9),
                "reason": "T型槽位置度影响工件夹具定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "工作台T型槽分布"
            },
            {
                "item": "对称度",
                "grade_range": (8, 10),
                "reason": "T型槽对称度影响定位键与槽的配合。",
                "standard_ref": "GB/T 1184",
                "application": "与位置度配合"
            },
        ],
    },
    "丝杠类": {
        "丝杠支承轴颈": [
            {
                "item": "圆度",
                "grade_range": (5, 7),
                "reason": "支承轴颈圆度误差直接影响丝杠运转精度和反向间隙。",
                "standard_ref": "GB/T 1184",
                "application": "精密丝杠两端轴颈"
            },
            {
                "item": "圆柱度",
                "grade_range": (5, 7),
                "reason": "圆柱度与圆度配合控制轴颈形状精度。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度同时控制"
            },
            {
                "item": "径向圆跳动",
                "grade_range": (5, 7),
                "reason": "支承轴颈跳动直接影响丝杠回转精度和定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "丝杠支承轴颈"
            },
            {
                "item": "同轴度（两轴颈间）",
                "grade_range": (5, 7),
                "reason": "两支承轴颈同轴度误差影响丝杠运转平稳性和轴承寿命。",
                "standard_ref": "GB/T 1184",
                "application": "两端轴颈"
            },
        ],
        "丝杠螺纹部分": [
            {
                "item": "同轴度（螺纹轴线对支承轴颈）",
                "grade_range": (5, 7),
                "reason": "螺纹轴线对支承轴颈的同轴度误差是产生螺距累积误差的主要原因。",
                "standard_ref": "GB/T 1184",
                "application": "滚珠丝杠、梯形丝杠"
            },
            {
                "item": "圆跳动（牙侧面对轴线）",
                "grade_range": (5, 7),
                "reason": "螺纹牙侧面跳动反映螺距误差和牙形误差的综合影响。",
                "standard_ref": "GB/T 1184",
                "application": "精密丝杠检验"
            },
        ],
        "螺母安装面": [
            {
                "item": "垂直度（安装面对轴线）",
                "grade_range": (6, 8),
                "reason": "螺母安装面对丝杠轴线的垂直度影响螺母运动灵活性和使用寿命。",
                "standard_ref": "GB/T 1184",
                "application": "螺母支承面"
            },
            {
                "item": "平面度",
                "grade_range": (7, 9),
                "reason": "安装面平面度影响螺母定位精度。",
                "standard_ref": "GB/T 1184",
                "application": "与垂直度配合"
            },
        ],
    },
    "液压气动类": {
        "液压缸筒": [
            {
                "item": "圆度",
                "grade_range": (6, 9),
                "reason": "缸筒圆度误差直接影响活塞密封寿命和缸筒容积效率。",
                "standard_ref": "GB/T 1184",
                "application": "液压缸内孔、气缸筒"
            },
            {
                "item": "圆柱度",
                "grade_range": (6, 9),
                "reason": "圆柱度误差与直线度配合控制缸筒形状精度。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度、直线度配合"
            },
            {
                "item": "直线度",
                "grade_range": (6, 9),
                "reason": "缸筒直线度误差影响活塞杆运动平稳性和密封寿命。",
                "standard_ref": "GB/T 1184",
                "application": "长行程液压缸"
            },
        ],
        "活塞杆": [
            {
                "item": "圆度",
                "grade_range": (6, 8),
                "reason": "活塞杆圆度误差影响活塞密封效果和运动平稳性。",
                "standard_ref": "GB/T 1184",
                "application": "液压缸活塞杆"
            },
            {
                "item": "圆柱度",
                "grade_range": (6, 8),
                "reason": "圆柱度与圆度配合控制活塞杆形状精度。",
                "standard_ref": "GB/T 1184",
                "application": "与圆度同时控制"
            },
            {
                "item": "直线度",
                "grade_range": (6, 8),
                "reason": "活塞杆直线度误差影响密封件寿命和导向套磨损。",
                "standard_ref": "GB/T 1184",
                "application": "活塞杆全长"
            },
            {
                "item": "同轴度（工作面对支承面）",
                "grade_range": (6, 8),
                "reason": "活塞杆工作面对支承轴颈的同轴度影响密封件均匀磨损。",
                "standard_ref": "GB/T 1184",
                "application": "活塞杆"
            },
        ],
        "阀块安装面": [
            {
                "item": "平面度",
                "grade_range": (6, 8),
                "reason": "阀块安装面平面度直接影响密封效果，是液压系统可靠性的关键。",
                "standard_ref": "GB/T 1184",
                "application": "液压集成块安装面"
            },
            {
                "item": "垂直度（安装面孔对安装面）",
                "grade_range": (7, 9),
                "reason": "安装孔轴线对安装面的垂直度影响密封圈压缩量。",
                "standard_ref": "GB/T 1184",
                "application": "阀块安装孔"
            },
            {
                "item": "位置度（安装孔间距）",
                "grade_range": (7, 9),
                "reason": "安装孔位置度误差影响阀门装配和密封效果。",
                "standard_ref": "GB/T 1184",
                "application": "安装孔分布"
            },
        ],
        "油缸端盖": [
            {
                "item": "平面度",
                "grade_range": (6, 8),
                "reason": "端盖配合面平面度是保证密封效果的首要条件。",
                "standard_ref": "GB/T 1184",
                "application": "液压缸前后端盖"
            },
            {
                "item": "同轴度（配合面对支承面）",
                "grade_range": (6, 8),
                "reason": "配合面对支承面的同轴度影响活塞杆运动对中。",
                "standard_ref": "GB/T 1184",
                "application": "油缸导向套孔"
            },
            {
                "item": "垂直度（配合面对轴线）",
                "grade_range": (6, 8),
                "reason": "配合面对轴线垂直度影响密封件受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "端盖配合面"
            },
        ],
    },
    "通用零件": {
        "键连接（轴/孔键槽）": [
            {
                "item": "对称度",
                "grade_range": (7, 9),
                "reason": "键槽对称度误差是最常见的键连接失效原因，会导致键和键槽早期损坏。",
                "standard_ref": "GB/T 1184",
                "application": "平键槽、半圆键槽、楔键槽"
            },
            {
                "item": "平行度（键槽侧面对轴线）",
                "grade_range": (7, 9),
                "reason": "键槽侧面平行度误差影响键的装配和受力均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "与对称度同时控制"
            },
            {
                "item": "位置度（花键）",
                "grade_range": (7, 9),
                "reason": "花键位置度误差影响花键副装配和承载均匀性。",
                "standard_ref": "GB/T 1184",
                "application": "矩形花键、渐开线花键"
            },
        ],
        "退刀槽/砂轮越程槽": [
            {
                "item": "圆度",
                "grade_range": (8, 10),
                "reason": "退刀槽圆度误差影响磨削工艺和零件功能。",
                "standard_ref": "GB/T 1184",
                "application": "轴肩退刀槽、孔内退刀槽"
            },
            {
                "item": "宽度尺寸（可用尺寸公差控制）",
                "grade_range": (9, 11),
                "reason": "退刀槽宽度影响刀具退出和磨削工艺。",
                "standard_ref": "GB/T 1800",
                "application": "砂轮越程槽"
            },
        ],
        "倒角/圆角": [
            {
                "item": "圆度（圆角）",
                "grade_range": (8, 11),
                "reason": "圆角半径误差影响应力集中系数和装配。",
                "standard_ref": "GB/T 1184",
                "application": "轴肩圆角、孔口圆角"
            },
        ],
        "中心孔": [
            {
                "item": "同轴度（中心孔对基准轴颈）",
                "grade_range": (6, 8),
                "reason": "中心孔同轴度误差影响工件的再加工精度和顶尖支承稳定性。",
                "standard_ref": "GB/T 1184",
                "application": "轴类零件中心孔"
            },
            {
                "item": "位置度（多中心孔）",
                "grade_range": (7, 9),
                "reason": "两端中心孔位置度误差影响工件调头装夹精度。",
                "standard_ref": "GB/T 1184",
                "application": "长轴两端中心孔"
            },
        ],
        "焊接件（机加工面）": [
            {
                "item": "平面度",
                "grade_range": (8, 11),
                "reason": "焊接件机加工面平面度受焊接变形影响。",
                "standard_ref": "GB/T 1184",
                "application": "焊接结构件加工面"
            },
            {
                "item": "平行度",
                "grade_range": (8, 11),
                "reason": "焊接件平行度受焊接变形影响，需要多次校正。",
                "standard_ref": "GB/T 1184",
                "application": "焊接床身、焊接箱体"
            },
            {
                "item": "垂直度",
                "grade_range": (8, 11),
                "reason": "焊接件垂直度受焊接变形影响。",
                "standard_ref": "GB/T 1184",
                "application": "焊接支架"
            },
        ],
        "冲压件": [
            {
                "item": "平面度",
                "grade_range": (8, 11),
                "reason": "冲压件回弹变形影响平面度。",
                "standard_ref": "GB/T 1184",
                "application": "冲压盖板、支架"
            },
            {
                "item": "位置度（孔对边缘）",
                "grade_range": (8, 11),
                "reason": "冲压孔位置度影响装配。",
                "standard_ref": "GB/T 1184",
                "application": "冲压件安装孔"
            },
            {
                "item": "对称度",
                "grade_range": (8, 11),
                "reason": "冲压件对称度影响外观和装配。",
                "standard_ref": "GB/T 1184",
                "application": "对称形状冲压件"
            },
        ],
        "铸件（机加工面）": [
            {
                "item": "平面度",
                "grade_range": (8, 11),
                "reason": "铸件机加工面平面度受铸造变形和夹砂影响。",
                "standard_ref": "GB/T 1184",
                "application": "铸造箱体面、支架面"
            },
            {
                "item": "平行度",
                "grade_range": (8, 11),
                "reason": "铸件平行度受铸造变形影响。",
                "standard_ref": "GB/T 1184",
                "application": "铸造基准面"
            },
            {
                "item": "同轴度（铸孔）",
                "grade_range": (8, 11),
                "reason": "铸造孔同轴度误差受芯子偏移影响。",
                "standard_ref": "GB/T 1184",
                "application": "铸造轴承孔"
            },
        ],
    },
}
