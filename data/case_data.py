# -*- coding: utf-8 -*-
"""
常见机械结构公差案例库 + 防错设计检查清单 + 内置材料库
"""

# ==================== 常见机械结构公差案例库 ====================
MECHANICAL_CASES = [
    # ---------- 轴承安装 ----------
    {
        "category": "轴承安装",
        "icon": "⚙️",
        "cases": [
            {
                "name": "深沟球轴承（内圈旋转）安装",
                "description": "最常见的轴承安装方式，内圈随轴旋转，外圈固定在轴承座中。",
                "svg_diagram": """
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <!-- 轴 -->
  <rect x="140" y="75" width="200" height="30" fill="#6B7280" stroke="#374151" stroke-width="2"/>
  <text x="330" y="97" font-size="11" fill="#fff">轴</text>
  <!-- 轴承外圈 -->
  <rect x="180" y="55" width="80" height="70" fill="#FCD34D" stroke="#F59E0B" stroke-width="2" rx="5"/>
  <text x="210" y="93" font-size="10" fill="#78350F">外圈</text>
  <!-- 轴承内圈 -->
  <rect x="185" y="70" width="70" height="40" fill="#93C5FD" stroke="#3B82F6" stroke-width="2" rx="3"/>
  <text x="205" y="93" font-size="10" fill="#1E40AF">内圈</text>
  <!-- 滚动体 -->
  <circle cx="220" cy="90" r="8" fill="#E5E7EB" stroke="#9CA3AF" stroke-width="1.5"/>
  <circle cx="240" cy="90" r="8" fill="#E5E7EB" stroke="#9CA3AF" stroke-width="1.5"/>
  <!-- 轴承座孔 -->
  <rect x="160" y="45" width="120" height="90" fill="none" stroke="#EF4444" stroke-width="2" stroke-dasharray="5,3" rx="8"/>
  <text x="180" y="38" font-size="10" fill="#EF4444">轴承座孔 H7</text>
  <!-- 配合标注 -->
  <line x1="170" y1="110" x2="170" y2="140" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="165" y1="140" x2="175" y2="140" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="255" y1="110" x2="255" y2="140" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="250" y1="140" x2="260" y2="140" stroke="#EF4444" stroke-width="1.5"/>
  <text x="195" y="155" font-size="9" fill="#EF4444" text-anchor="middle">过盈/过渡配合</text>
  <!-- 轴肩 -->
  <rect x="340" y="70" width="15" height="40" fill="#6B7280" stroke="#374151" stroke-width="2"/>
  <text x="345" y="158" font-size="9" fill="#374151">轴肩</text>
  <!-- 旋转箭头 -->
  <path d="M150 50 A30 30 0 0 1 150 110" fill="none" stroke="#10B981" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#10B981"/>
    </marker>
  </defs>
  <text x="130" y="45" font-size="9" fill="#10B981">旋转</text>
</svg>
""",
                "design_points": [
                    "轴与轴承内圈采用过渡配合或轻过盈配合（如 j5、k5、m5）",
                    "轴承座孔与轴承外圈采用间隙配合或过渡配合（如 J7、H7）",
                    "轴肩直径应大于轴承内圈外径，确保轴向定位",
                    "轴肩圆角半径 < 轴承内圈圆角半径，避免干涉",
                    "轴承座挡肩圆角半径 < 轴承外圈圆角半径",
                ],
                "tolerance_values": [
                    {"部位": "轴（轴承位）", "公差带": "k5 / m5", "说明": "IT5级，保证与内圈轻过盈配合"},
                    {"部位": "轴承座孔", "公差带": "H7 / J7", "说明": "IT7级，外圈可轴向游动"},
                    {"部位": "轴肩端面跳动", "公差带": "≤0.015mm", "说明": "防止轴承倾斜"},
                    {"部位": "座孔挡肩端面跳动", "公差带": "≤0.02mm", "说明": "保证轴承座端面定位精度"},
                    {"部位": "配合面粗糙度（轴）", "公差带": "Ra 0.8", "说明": "磨削加工"},
                    {"部位": "配合面粗糙度（孔）", "公差带": "Ra 1.6", "说明": "精镗或磨削"},
                ],
                "common_mistakes": [
                    "轴公差带选得过松（如h7），导致内圈蠕变（跑圈）",
                    "座孔公差带选得过紧（如K7），导致外圈无法补偿热膨胀",
                    "忘记标注轴肩和座孔挡肩的端面跳动",
                    "轴肩圆角过大，与轴承倒角干涉",
                ],
            },
            {
                "name": "半圆键连接",
                "description": "适用于锥形轴端连接，键在轴槽中可摆动以适应轮毂斜度。",
                "svg_diagram": """
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <!-- 轴 -->
  <rect x="50" y="75" width="300" height="30" fill="#6B7280" stroke="#374151" stroke-width="2"/>
  <text x="200" y="97" font-size="11" fill="#fff" text-anchor="middle">轴</text>
  <!-- 键槽 -->
  <path d="M160 75 Q160 95 180 95 Q200 95 200 75" fill="#FCD34D" stroke="#F59E0B" stroke-width="2"/>
  <!-- 键 -->
  <path d="M165 75 Q165 85 180 85 Q195 85 195 75" fill="#FBBF24" stroke="#D97706" stroke-width="1.5"/>
  <text x="180" y="72" font-size="9" fill="#92400E" text-anchor="middle">键</text>
  <!-- 键槽标注 -->
  <line x1="165" y1="110" x2="165" y2="130" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="195" y1="110" x2="195" y2="130" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="180" y1="130" x2="180" y2="145" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="175" y1="145" x2="185" y2="145" stroke="#EF4444" stroke-width="1.5"/>
  <text x="180" y="160" font-size="9" fill="#EF4444" text-anchor="middle">b (键宽)</text>
  <!-- 尺寸标注 -->
  <text x="70" y="60" font-size="10" fill="#374151">t₁（轴槽深）</text>
  <text x="250" y="60" font-size="10" fill="#374151">键宽 b N9</text>
  <!-- 公差带标注 -->
  <rect x="165" y="140" width="30" height="8" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/>
  <text x="180" y="170" font-size="8" fill="#EF4444" text-anchor="middle">N9</text>
</svg>
""",
                "design_points": [
                    "键宽与轴槽宽配合同平键（N9/h9）",
                    "轴槽深度按 GB/T 1098 选取",
                    "半圆键的半径 R 需与轴槽匹配",
                    "适用于轻载、低速传动场合",
                ],
                "tolerance_values": [
                    {"部位": "键宽 b", "公差带": "h9", "说明": "标准件"},
                    {"部位": "轴槽宽 b", "公差带": "N9", "说明": "过渡配合"},
                    {"部位": "轮毂槽宽 b", "公差带": "Js9 / D10", "说明": "一般/较松"},
                    {"部位": "键槽对称度", "公差带": "0.02~0.04mm", "说明": "视键宽"},
                ],
                "common_mistakes": [
                    "用于重载场合（半圆键承载能力有限）",
                    "轴槽深度不够，键容易脱落",
                ],
            },
            {
                "name": "O形密封圈沟槽设计",
                "description": "O形圈是最常见的密封方式，沟槽尺寸精度直接影响密封效果。",
                "svg_diagram": """
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <!-- 缸体/孔 -->
  <rect x="80" y="50" width="240" height="80" fill="#E5E7EB" stroke="#374151" stroke-width="2"/>
  <!-- 沟槽 -->
  <rect x="120" y="65" width="160" height="50" fill="#93C5FD" stroke="#3B82F6" stroke-width="2"/>
  <!-- O形圈 -->
  <ellipse cx="200" cy="90" rx="55" ry="20" fill="#FCD34D" stroke="#F59E0B" stroke-width="2"/>
  <!-- 压缩变形 -->
  <ellipse cx="200" cy="90" rx="45" ry="15" fill="#FEF3C7" stroke="#FBBF24" stroke-width="1" stroke-dasharray="3,2"/>
  <!-- 标注 -->
  <line x1="120" y1="130" x2="120" y2="155" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="280" y1="130" x2="280" y2="155" stroke="#EF4444" stroke-width="1.5"/>
  <text x="200" y="165" font-size="9" fill="#EF4444" text-anchor="middle">B（沟槽宽度）</text>
  <line x1="310" y1="65" x2="350" y2="65" stroke="#10B981" stroke-width="1.5"/>
  <line x1="310" y1="115" x2="350" y2="115" stroke="#10B981" stroke-width="1.5"/>
  <line x1="345" y1="65" x2="345" y2="115" stroke="#10B981" stroke-width="1.5"/>
  <text x="355" y="95" font-size="9" fill="#10B981">H</text>
  <text x="355" y="105" font-size="9" fill="#10B981">(沟槽深度)</text>
  <!-- 说明 -->
  <text x="100" y="45" font-size="9" fill="#374151">缸体/孔</text>
  <text x="185" y="100" font-size="9" fill="#92400E" text-anchor="middle">O形圈</text>
  <!-- 压缩率标注 -->
  <path d="M145 35 L145 50" stroke="#8B5CF6" stroke-width="1.5"/>
  <path d="M145 50 L155 50" stroke="#8B5CF6" stroke-width="1.5"/>
  <path d="M255 35 L255 50" stroke="#8B5CF6" stroke-width="1.5"/>
  <path d="M255 50 L245 50" stroke="#8B5CF6" stroke-width="1.5"/>
  <text x="200" y="32" font-size="8" fill="#8B5CF6" text-anchor="middle">压缩量 15%~25%</text>
</svg>
""",
                "design_points": [
                    "沟槽深度 H 按密封圈压缩率 15%~25% 计算",
                    "沟槽宽度 B 一般为密封圈线径 d 的 1.3~1.5 倍",
                    "沟槽底面和侧面粗糙度 Ra 0.8~1.6（太光滑会打滑）",
                    "沟槽圆角 R0.1~0.3，避免切伤密封圈",
                    "配合面（轴或孔）粗糙度 Ra 0.4~0.8",
                ],
                "tolerance_values": [
                    {"部位": "沟槽深度 H", "公差带": "+0.05/0", "说明": "控制压缩率"},
                    {"部位": "沟槽宽度 B", "公差带": "+0.1/0", "说明": "保证密封圈有膨胀空间"},
                    {"部位": "沟槽底面粗糙度", "公差带": "Ra 1.6", "说明": "车削即可"},
                    {"部位": "密封配合面粗糙度", "公差带": "Ra 0.4~0.8", "说明": "磨削"},
                    {"部位": "沟槽圆角", "公差带": "R0.1~0.3", "说明": "避免切伤O圈"},
                ],
                "common_mistakes": [
                    "沟槽太深，压缩量不够导致泄漏",
                    "沟槽太浅，压缩量过大导致O圈永久变形",
                    "沟槽表面太粗糙，划伤密封圈",
                    "忽略温度对密封圈材料硬度的影响",
                ],
            },
        ],
    },
    # ---------- 键连接 ----------
    {
        "category": "键连接",
        "icon": "🔑",
        "cases": [
            {
                "name": "普通平键连接（圆头/平头）",
                "description": "最常用的轴毂连接方式，通过键传递扭矩，键两侧面为工作面。",
                "svg_diagram": """
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <!-- 轴 -->
  <rect x="100" y="75" width="200" height="30" fill="#6B7280" stroke="#374151" stroke-width="2"/>
  <text x="200" y="97" font-size="11" fill="#fff" text-anchor="middle">轴</text>
  <!-- 轮毂 -->
  <rect x="150" y="60" width="100" height="60" fill="#93C5FD" stroke="#3B82F6" stroke-width="2" rx="3"/>
  <text x="200" y="87" font-size="10" fill="#1E40AF" text-anchor="middle">轮毂</text>
  <!-- 键槽（轴上） -->
  <rect x="145" y="95" width="110" height="10" fill="#FCD34D" stroke="#F59E0B" stroke-width="1.5"/>
  <!-- 键 -->
  <rect x="150" y="93" width="100" height="14" fill="#FBBF24" stroke="#D97706" stroke-width="2" rx="2"/>
  <text x="200" y="103" font-size="9" fill="#92400E" text-anchor="middle">平键</text>
  <!-- 键槽（毂上） -->
  <rect x="155" y="60" width="90" height="10" fill="#FCD34D" stroke="#F59E0B" stroke-width="1.5"/>
  <!-- 尺寸标注 -->
  <line x1="145" y1="130" x2="145" y2="155" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="255" y1="130" x2="255" y2="155" stroke="#EF4444" stroke-width="1.5"/>
  <text x="200" y="168" font-size="9" fill="#EF4444" text-anchor="middle">b（键宽）</text>
  <!-- 公差标注 -->
  <text x="180" y="145" font-size="8" fill="#10B981">N9/h9</text>
  <!-- 扭矩方向 -->
  <path d="M80 60 Q60 90 80 120" fill="none" stroke="#10B981" stroke-width="2" marker-end="url(#arrow1)"/>
  <text x="45" y="90" font-size="9" fill="#10B981">扭矩</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#10B981"/>
    </marker>
  </defs>
</svg>
""",
                "design_points": [
                    "键宽与键槽宽采用过渡配合或较紧间隙配合（如 N9/js9）",
                    "键高与键槽深采用较松配合（键在槽中不卡死）",
                    "键槽对称度公差一般取 IT7~IT9 级",
                    "轴槽深 t1 和轮毂槽深 t2 按国标 GB/T 1095 选取",
                    "两个键槽如果轴向距离较远，需分别标注对称度",
                ],
                "tolerance_values": [
                    {"部位": "键宽 b", "公差带": "h9", "说明": "键为标准件，键宽 h9"},
                    {"部位": "轴槽宽 b", "公差带": "N9", "说明": "较紧配合，防止键侧晃动"},
                    {"部位": "轮毂槽宽 b", "公差带": "Js9 / D10", "说明": "一般配合/较松配合"},
                    {"部位": "键槽对称度", "公差带": "0.02~0.05mm", "说明": "视键宽和精度要求"},
                    {"部位": "键槽侧面粗糙度", "公差带": "Ra 3.2", "说明": "铣削或拉削"},
                    {"部位": "键槽底面粗糙度", "公差带": "Ra 6.3", "说明": "铣削"},
                ],
                "common_mistakes": [
                    "轮毂槽宽公差选得过紧（如 P9），导致装配困难",
                    "未标注键槽对称度，导致键偏载受力不均",
                    "键槽底部圆角过小，产生应力集中",
                    "忘记标注键槽深度尺寸及公差",
                ],
            },
        ],
    },
    # ---------- 销连接 ----------
    {
        "category": "销连接",
        "icon": "📌",
        "cases": [
            {
                "name": "圆柱销定位连接",
                "description": "用于零件精确定位，承受较小剪切力。",
                "svg_diagram": """
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <!-- 上零件 -->
  <rect x="100" y="60" width="200" height="40" fill="#93C5FD" stroke="#3B82F6" stroke-width="2"/>
  <text x="200" y="84" font-size="11" fill="#1E40AF" text-anchor="middle">上零件</text>
  <!-- 下零件 -->
  <rect x="100" y="100" width="200" height="40" fill="#6B7280" stroke="#374151" stroke-width="2"/>
  <text x="200" y="124" font-size="11" fill="#fff" text-anchor="middle">下零件</text>
  <!-- 销孔 -->
  <circle cx="200" cy="100" r="12" fill="#E5E7EB" stroke="#9CA3AF" stroke-width="2"/>
  <circle cx="200" cy="100" r="8" fill="#FCD34D" stroke="#F59E0B" stroke-width="1.5"/>
  <!-- 销 -->
  <rect x="192" y="50" width="16" height="100" fill="#FBBF24" stroke="#D97706" stroke-width="2" rx="2"/>
  <text x="200" y="45" font-size="9" fill="#92400E" text-anchor="middle">圆柱销</text>
  <text x="200" y="165" font-size="9" fill="#92400E" text-anchor="middle">m6/H7</text>
  <!-- 定位箭头 -->
  <line x1="250" y1="80" x2="280" y2="50" stroke="#10B981" stroke-width="1.5"/>
  <text x="285" y="48" font-size="9" fill="#10B981">定位销</text>
  <line x1="250" y1="120" x2="280" y2="150" stroke="#10B981" stroke-width="1.5"/>
  <text x="285" y="155" font-size="9" fill="#10B981">配钻铰</text>
  <!-- 圆角标注 -->
  <path d="M185 110 A8 8 0 0 0 185 125" fill="none" stroke="#EF4444" stroke-width="1"/>
  <text x="175" y="140" font-size="8" fill="#EF4444">R0.3</text>
</svg>
""",
                "design_points": [
                    "销孔需配钻铰，保证配合精度",
                    "一般配合：销 m6 / 孔 H7（过渡配合）",
                    "定位精度要求高时：销 h5 / 孔 H6 或销 n6 / 孔 H7",
                    "两被连接件需一起加工销孔（配钻）",
                    "销孔表面粗糙度 Ra 0.8~1.6",
                ],
                "tolerance_values": [
                    {"部位": "圆柱销", "公差带": "m6 / h5", "说明": "标准件"},
                    {"部位": "销孔", "公差带": "H7 / H6", "说明": "配钻铰"},
                    {"部位": "销孔粗糙度", "公差带": "Ra 0.8~1.6", "说明": "铰削"},
                    {"部位": "两销孔位置度", "公差带": "0.02~0.05mm", "说明": "视精度"},
                ],
                "common_mistakes": [
                    "两零件分别钻孔，导致销孔不同心",
                    "未标注配钻要求",
                    "销孔粗糙度不够，影响配合质量",
                ],
            },
        ],
    },
    # ---------- 齿轮传动 ----------
    {
        "category": "齿轮传动",
        "icon": "⚙️",
        "cases": [
            {
                "name": "圆柱齿轮轴系安装",
                "description": "齿轮在轴上的安装，需保证齿轮精度和传动平稳性。",
                "svg_diagram": """
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <!-- 轴 -->
  <rect x="80" y="85" width="240" height="20" fill="#6B7280" stroke="#374151" stroke-width="2"/>
  <text x="200" y="100" font-size="11" fill="#fff" text-anchor="middle">轴</text>
  <!-- 齿轮 -->
  <circle cx="200" cy="90" r="50" fill="#93C5FD" stroke="#3B82F6" stroke-width="2"/>
  <circle cx="200" cy="90" r="20" fill="#6B7280" stroke="#374151" stroke-width="2"/>
  <!-- 齿轮齿 -->
  <g fill="#93C5FD" stroke="#3B82F6" stroke-width="1.5">
    <rect x="196" y="38" width="8" height="15"/>
    <rect x="196" y="127" width="8" height="15"/>
    <rect x="148" y="86" width="15" height="8"/>
    <rect x="237" y="86" width="15" height="8"/>
    <rect x="158" y="50" width="12" height="8" transform="rotate(45 164 54)"/>
    <rect x="230" y="50" width="12" height="8" transform="rotate(-45 236 54)"/>
    <rect x="158" y="122" width="12" height="8" transform="rotate(-45 164 126)"/>
    <rect x="230" y="122" width="12" height="8" transform="rotate(45 236 126)"/>
  </g>
  <!-- 键槽 -->
  <rect x="170" y="100" width="60" height="8" fill="#FCD34D" stroke="#F59E0B" stroke-width="1"/>
  <!-- 轴承 -->
  <rect x="100" y="75" width="30" height="30" fill="#FCD34D" stroke="#F59E0B" stroke-width="2" rx="3"/>
  <rect x="270" y="75" width="30" height="30" fill="#FCD34D" stroke="#F59E0B" stroke-width="2" rx="3"/>
  <!-- 标注 -->
  <text x="200" y="20" font-size="10" fill="#1E40AF" text-anchor="middle">圆柱齿轮</text>
  <text x="200" y="160" font-size="9" fill="#374151" text-anchor="middle">齿轮孔 H7 / 轴 k5-m5</text>
  <text x="115" y="155" font-size="9" fill="#92400E">轴承</text>
  <text x="285" y="155" font-size="9" fill="#92400E">轴承</text>
  <!-- 扭矩方向 -->
  <path d="M310 60 A25 25 0 0 1 310 120" fill="none" stroke="#10B981" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="320" y="90" font-size="9" fill="#10B981">扭矩</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#10B981"/>
    </marker>
  </defs>
</svg>
""",
                "design_points": [
                    "齿轮与轴配合视工况：一般 k5/m5（固定）或 H7/f7（滑动）",
                    "齿轮基准端面跳动 ≤ 0.015~0.03mm（视精度等级）",
                    "齿轮径向跳动按齿轮精度等级确定",
                    "键槽对称度影响齿轮径向跳动，需严格控制",
                    "高速齿轮需做动平衡",
                ],
                "tolerance_values": [
                    {"部位": "轴（齿轮位）", "公差带": "k5 / m5", "说明": "固定连接"},
                    {"部位": "齿轮孔", "公差带": "H7", "说明": "IT7级"},
                    {"部位": "基准端面跳动", "公差带": "0.015~0.03mm", "说明": "视精度等级"},
                    {"部位": "键槽对称度", "公差带": "0.01~0.03mm", "说明": "高精度要求"},
                    {"部位": "齿面粗糙度", "公差带": "Ra 0.8~1.6", "说明": "磨齿/剃齿"},
                ],
                "common_mistakes": [
                    "齿轮端面跳动超差，导致传动不平稳",
                    "键槽对称度超差，导致齿轮偏心",
                    "高速齿轮未做动平衡，产生振动和噪声",
                ],
            },
        ],
    },
    # ---------- 导轨与滑动副 ----------
    {
        "category": "导轨与滑动副",
        "icon": "📏",
        "cases": [
            {
                "name": "平导轨配合",
                "description": "机床和精密设备中常见的直线导向结构。",
                "svg_diagram": """
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <!-- 下导轨（固定） -->
  <rect x="50" y="120" width="300" height="20" fill="#E5E7EB" stroke="#374151" stroke-width="2"/>
  <text x="200" y="135" font-size="11" fill="#374151" text-anchor="middle">下导轨</text>
  <!-- 滑动块 -->
  <rect x="100" y="70" width="200" height="45" fill="#93C5FD" stroke="#3B82F6" stroke-width="2" rx="3"/>
  <text x="200" y="97" font-size="11" fill="#1E40AF" text-anchor="middle">滑动块</text>
  <!-- 镶条（调整间隙） -->
  <rect x="290" y="115" width="20" height="15" fill="#FCD34D" stroke="#F59E0B" stroke-width="2"/>
  <text x="300" y="125" font-size="8" fill="#92400E" text-anchor="middle">镶</text>
  <!-- 润滑油槽 -->
  <rect x="130" y="90" width="40" height="3" fill="#6B7280"/>
  <rect x="180" y="90" width="40" height="3" fill="#6B7280"/>
  <rect x="230" y="90" width="40" height="3" fill="#6B7280"/>
  <!-- 运动方向 -->
  <line x1="50" y1="55" x2="350" y2="55" stroke="#10B981" stroke-width="2" stroke-dasharray="8,4"/>
  <path d="M340 45 L350 55 L340 65" fill="none" stroke="#10B981" stroke-width="2"/>
  <text x="200" y="45" font-size="9" fill="#10B981" text-anchor="middle">运动方向</text>
  <!-- 间隙标注 -->
  <line x1="100" y1="108" x2="100" y2="125" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="300" y1="108" x2="300" y2="125" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="95" y1="120" x2="105" y2="120" stroke="#EF4444" stroke-width="1.5"/>
  <line x1="295" y1="120" x2="305" y2="120" stroke="#EF4444" stroke-width="1.5"/>
  <text x="200" y="160" font-size="9" fill="#EF4444" text-anchor="middle">配合间隙 0.01~0.05mm</text>
  <!-- 直线度标注 -->
  <path d="M50 145 Q200 140 350 145" fill="none" stroke="#8B5CF6" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="200" y="170" font-size="8" fill="#8B5CF6" text-anchor="middle">导轨直线度 0.01~0.05mm/m</text>
</svg>
""",
                "design_points": [
                    "导轨面直线度公差按精度等级选取（一般 0.01~0.05mm/m）",
                    "导轨面平行度公差控制在 0.01~0.03mm 以内",
                    "配合间隙：一般 0.01~0.05mm（需镶条调整）",
                    "导轨面粗糙度 Ra 0.4~0.8（磨削）",
                    "润滑油槽应合理分布",
                ],
                "tolerance_values": [
                    {"部位": "导轨面直线度", "公差带": "0.01~0.05mm/m", "说明": "视精度等级"},
                    {"部位": "导轨面平行度", "公差带": "0.01~0.03mm", "说明": "全长"},
                    {"部位": "配合间隙", "公差带": "0.01~0.05mm", "说明": "镶条调整"},
                    {"部位": "导轨面粗糙度", "公差带": "Ra 0.4~0.8", "说明": "磨削"},
                ],
                "common_mistakes": [
                    "导轨面直线度超差，导致运动不平稳",
                    "配合间隙过大，失去导向精度",
                    "未设计润滑油槽，导致导轨面拉伤",
                ],
            },
        ],
    },
]


# ==================== 防错设计检查清单 ====================
POKAYOKE_CHECKLIST = [
    {
        "category": "对称性与防反装",
        "icon": "🔄",
        "checks": [
            {
                "name": "零件对称性检查",
                "description": "检查零件是否为完全对称结构，避免装配时方向装反。",
                "items": [
                    {"check": "零件外形是否完全对称（旋转180°后是否一致）", "level": "必须检查", "tip": "如果外形对称但内部孔位/特征不对称，需增加防错特征"},
                    {"check": "非对称零件是否有明显的视觉防错标识", "level": "推荐", "tip": "如倒角大小不同、标记箭头、颜色区分等"},
                    {"check": "非对称零件是否设计了定位销或防错凸台", "level": "推荐", "tip": "定位销是最可靠的防错方式，建议在关键装配处使用"},
                    {"check": "装配方向是否唯一且明确", "level": "必须检查", "tip": "理想情况下零件只能以一个方向装入"},
                ],
            },
            {
                "name": "不对称定位销设计",
                "description": "通过不对称定位销确保零件只能以正确方向装配。",
                "items": [
                    {"check": "定位销数量是否为奇数（推荐1个或3个）", "level": "推荐", "tip": "2个对称定位销无法防反装，奇数个可确保方向唯一"},
                    {"check": "定位销位置是否偏心布置", "level": "推荐", "tip": "偏心布置使零件只能以一个方向装入"},
                    {"check": "定位销直径是否与普通螺栓孔明显不同", "level": "推荐", "tip": "避免操作者将定位销与螺栓混淆"},
                    {"check": "定位销是否有足够的导入倒角", "level": "必须检查", "tip": "导入倒角 15°~30°，便于装配导向"},
                ],
            },
        ],
    },
    {
        "category": "装配防错",
        "icon": "🔧",
        "checks": [
            {
                "name": "螺纹连接防错",
                "description": "防止螺栓错装、漏装、预紧不足。",
                "items": [
                    {"check": "不同规格螺栓是否使用了不同的孔径或间距", "level": "推荐", "tip": "避免M8和M10螺栓孔间距相同导致错装"},
                    {"check": "关键螺栓是否有扭矩标记线", "level": "推荐", "tip": "拧紧后画线标记，便于巡检确认是否松动"},
                    {"check": "螺栓长度是否合适（露出螺母 1~2 扣）", "level": "必须检查", "tip": "螺栓过长可能干涉其他零件，过短则强度不足"},
                    {"check": "是否有防止螺栓遗忘的设计（如盲孔底面）", "level": "推荐", "tip": "螺栓通孔设计可避免操作者忘记装螺栓"},
                ],
            },
            {
                "name": "密封面防错",
                "description": "防止密封件漏装、装反或损坏。",
                "items": [
                    {"check": "密封槽是否有单向导入角", "level": "推荐", "tip": "单向导入角确保密封圈只能以正确方向装入"},
                    {"check": "密封件是否在零件装配顺序中难以遗漏", "level": "必须检查", "tip": "如果密封件在封闭空间内，需设计检查口"},
                    {"check": "密封面是否有防磕碰保护设计", "level": "推荐", "tip": "装配过程中密封面容易磕碰，需设计保护结构"},
                ],
            },
        ],
    },
    {
        "category": "公差标注防错",
        "icon": "📐",
        "checks": [
            {
                "name": "关键尺寸链完整性",
                "description": "确保影响装配和功能的关键尺寸链完整且无遗漏。",
                "items": [
                    {"check": "装配后的关键间隙/过盈是否在尺寸链中完整体现", "level": "必须检查", "tip": "如轴承游隙、齿轮侧隙等必须通过尺寸链计算验证"},
                    {"check": "尺寸链中是否包含了所有组成环（含垫片、O圈等）", "level": "必须检查", "tip": "遗漏任何一个组成环都可能导致计算错误"},
                    {"check": "最短尺寸链原则是否得到遵守", "level": "推荐", "tip": "减少组成环数量可降低累积误差"},
                    {"check": "封闭环公差是否合理分配到各组成环", "level": "必须检查", "tip": "等公差法或等精度法分配，关键环分配较紧公差"},
                ],
            },
            {
                "name": "基准选择合理性",
                "description": "确保设计基准、加工基准、检测基准统一。",
                "items": [
                    {"check": "设计基准是否与加工基准一致", "level": "推荐", "tip": "基准不重合会导致基准转换误差"},
                    {"check": "设计基准是否与装配基准一致", "level": "推荐", "tip": "装配基准是功能要求的直接体现"},
                    {"check": "是否避免了基准过约束（过多基准）", "level": "必须检查", "tip": "基准数量应最少且充分，一般 2~3 个"},
                    {"check": "基准面的加工精度是否高于被测要素", "level": "必须检查", "tip": "基准面本身精度不够会导致测量结果不可靠"},
                ],
            },
        ],
    },
    {
        "category": "工艺与装配防错",
        "icon": "🏭",
        "checks": [
            {
                "name": "加工可行性检查",
                "description": "确保设计的公差要求在现有工艺条件下可以实现。",
                "items": [
                    {"check": "公差等级是否与加工工艺能力匹配", "level": "必须检查", "tip": "如 IT5 需磨削，IT7 可精车，IT11 可粗车"},
                    {"check": "是否避免了在深孔或狭窄空间标注高精度公差", "level": "推荐", "tip": "深孔加工精度难以保证，应适当放宽公差"},
                    {"check": "是否考虑了热处理变形对公差的影响", "level": "推荐", "tip": "淬火后需磨削的表面应预留加工余量"},
                    {"check": "同一零件上的公差等级差异是否过大", "level": "推荐", "tip": "差异过大会增加加工成本和装夹次数"},
                ],
            },
            {
                "name": "装配干涉检查",
                "description": "确保零件装配过程中不会发生干涉。",
                "items": [
                    {"check": "最大实体状态下的零件是否会发生干涉", "level": "必须检查", "tip": "孔最小+轴最大=最紧配合状态，需验证是否可装配"},
                    {"check": "螺栓头/螺母是否有足够的扳手空间", "level": "必须检查", "tip": "参考 GB/T 152.4 螺栓/螺母的扳手空间"},
                    {"check": "零件装入路径上是否有干涉", "level": "必须检查", "tip": "考虑零件装入角度和路径，不能只看最终位置"},
                    {"check": "密封件/弹簧等弹性件压缩后是否超出设计空间", "level": "推荐", "tip": "弹性件压缩后的尺寸需在装配空间内"},
                ],
            },
        ],
    },
]


# ==================== 内置材料库 ====================
MATERIAL_PROPERTIES = [
    # 碳钢及合金钢
    {"category": "碳钢及合金钢", "material": "Q235A", "density": 7.85, "elastic_modulus": 206, "yield_strength": 235, "tensile_strength": 375, "alpha": 11.7, "poisson_ratio": 0.30, "note": "普通结构钢，最常用"},
    {"category": "碳钢及合金钢", "material": "Q355B", "density": 7.85, "elastic_modulus": 206, "yield_strength": 355, "tensile_strength": 490, "alpha": 11.7, "poisson_ratio": 0.30, "note": "低合金高强度钢"},
    {"category": "碳钢及合金钢", "material": "45钢", "density": 7.85, "elastic_modulus": 206, "yield_strength": 355, "tensile_strength": 600, "alpha": 11.6, "poisson_ratio": 0.30, "note": "优质碳素结构钢，调质后使用"},
    {"category": "碳钢及合金钢", "material": "40Cr", "density": 7.85, "elastic_modulus": 211, "yield_strength": 785, "tensile_strength": 980, "alpha": 11.0, "poisson_ratio": 0.30, "note": "合金结构钢，调质处理"},
    {"category": "碳钢及合金钢", "material": "GCr15", "density": 7.80, "elastic_modulus": 219, "yield_strength": 518, "tensile_strength": 725, "alpha": 13.0, "poisson_ratio": 0.30, "note": "轴承钢，滚动轴承专用"},
    {"category": "碳钢及合金钢", "material": "20CrMnTi", "density": 7.80, "elastic_modulus": 207, "yield_strength": 835, "tensile_strength": 1080, "alpha": 11.0, "poisson_ratio": 0.30, "note": "渗碳齿轮钢"},
    {"category": "碳钢及合金钢", "material": "42CrMo", "density": 7.85, "elastic_modulus": 212, "yield_strength": 930, "tensile_strength": 1080, "alpha": 11.2, "poisson_ratio": 0.30, "note": "高强度合金钢，大型齿轮/轴"},
    # 灰铸铁
    {"category": "灰铸铁", "material": "HT200", "density": 7.20, "elastic_modulus": 130, "yield_strength": 200, "tensile_strength": 200, "alpha": 10.5, "poisson_ratio": 0.25, "note": "普通灰铸铁，中等载荷零件"},
    {"category": "灰铸铁", "material": "HT250", "density": 7.25, "elastic_modulus": 135, "yield_strength": 250, "tensile_strength": 250, "alpha": 10.5, "poisson_ratio": 0.25, "note": "较高强度灰铸铁"},
    {"category": "灰铸铁", "material": "HT300", "density": 7.30, "elastic_modulus": 145, "yield_strength": 300, "tensile_strength": 300, "alpha": 10.5, "poisson_ratio": 0.25, "note": "高强度灰铸铁，床身/箱体"},
    # 球墨铸铁
    {"category": "球墨铸铁", "material": "QT400-18", "density": 7.10, "elastic_modulus": 170, "yield_strength": 250, "tensile_strength": 400, "alpha": 11.0, "poisson_ratio": 0.28, "note": "高韧性球铁"},
    {"category": "球墨铸铁", "material": "QT500-7", "density": 7.10, "elastic_modulus": 175, "yield_strength": 320, "tensile_strength": 500, "alpha": 11.0, "poisson_ratio": 0.28, "note": "中等强度球铁"},
    {"category": "球墨铸铁", "material": "QT600-3", "density": 7.10, "elastic_modulus": 180, "yield_strength": 370, "tensile_strength": 600, "alpha": 11.0, "poisson_ratio": 0.28, "note": "高强度球铁，可替代锻钢"},
    # 铝合金
    {"category": "铝合金", "material": "6061-T6", "density": 2.70, "elastic_modulus": 69, "yield_strength": 240, "tensile_strength": 260, "alpha": 23.6, "poisson_ratio": 0.33, "note": "常用铝合金，可热处理强化"},
    {"category": "铝合金", "material": "7075-T6", "density": 2.81, "elastic_modulus": 72, "yield_strength": 503, "tensile_strength": 572, "alpha": 23.4, "poisson_ratio": 0.33, "note": "高强度航空铝合金"},
    {"category": "铝合金", "material": "ZL104", "density": 2.65, "elastic_modulus": 70, "yield_strength": 170, "tensile_strength": 220, "alpha": 22.0, "poisson_ratio": 0.33, "note": "铸造铝合金"},
    # 铜合金
    {"category": "铜合金", "material": "H62", "density": 8.43, "elastic_modulus": 100, "yield_strength": 380, "tensile_strength": 380, "alpha": 20.2, "poisson_ratio": 0.35, "note": "普通黄铜，H62为半硬态"},
    {"category": "铜合金", "material": "HPb59-1", "density": 8.50, "elastic_modulus": 100, "yield_strength": 420, "tensile_strength": 450, "alpha": 20.5, "poisson_ratio": 0.35, "note": "铅黄铜，易切削"},
    {"category": "铜合金", "material": "QSn6.5-0.1", "density": 8.80, "elastic_modulus": 110, "yield_strength": 545, "tensile_strength": 635, "alpha": 18.2, "poisson_ratio": 0.35, "note": "锡青铜，弹性元件"},
    {"category": "铜合金", "material": "QA19-2", "density": 7.60, "elastic_modulus": 110, "yield_strength": 450, "tensile_strength": 600, "alpha": 17.0, "poisson_ratio": 0.35, "note": "铝青铜，高强度耐磨"},
    # 不锈钢
    {"category": "不锈钢", "material": "304", "density": 8.00, "elastic_modulus": 193, "yield_strength": 205, "tensile_strength": 520, "alpha": 17.3, "poisson_ratio": 0.29, "note": "奥氏体不锈钢，食品/化工"},
    {"category": "不锈钢", "material": "316", "density": 8.00, "elastic_modulus": 193, "yield_strength": 205, "tensile_strength": 530, "alpha": 16.0, "poisson_ratio": 0.29, "note": "耐腐蚀不锈钢，耐海水"},
    {"category": "不锈钢", "material": "440C", "density": 7.75, "elastic_modulus": 200, "yield_strength": 415, "tensile_strength": 760, "alpha": 10.5, "poisson_ratio": 0.28, "note": "马氏体不锈钢，轴承/刀具"},
    # 钛合金
    {"category": "钛合金", "material": "TC4 (Ti-6Al-4V)", "density": 4.45, "elastic_modulus": 110, "yield_strength": 880, "tensile_strength": 950, "alpha": 9.0, "poisson_ratio": 0.34, "note": "航空钛合金，轻质高强"},
    # 其他
    {"category": "其他金属", "material": "ZG230-450", "density": 7.80, "elastic_modulus": 202, "yield_strength": 230, "tensile_strength": 450, "alpha": 12.0, "poisson_ratio": 0.30, "note": "铸钢，焊接结构件"},
    {"category": "其他金属", "material": "W18Cr4V", "density": 8.70, "elastic_modulus": 220, "yield_strength": 350, "tensile_strength": 750, "alpha": 11.0, "poisson_ratio": 0.28, "note": "高速钢，刀具材料"},
]

# 单位说明
MATERIAL_UNITS = {
    "density": "g/cm³",
    "elastic_modulus": "GPa",
    "yield_strength": "MPa",
    "tensile_strength": "MPa",
    "alpha": "×10⁻⁶/°C",
}
