# -*- coding: utf-8 -*-
"""
形位公差推荐模块
"""

import streamlit as st

from data.geo_tolerance_data import GEOMETRIC_TOLERANCE_RECOMMENDATIONS
from modules.utils import lookup_geo_tolerance, generate_gdandt_annotation_svg


def render_geometric_tolerance_tab():
    """渲染形位公差推荐选项卡 - 全新友好界面"""
    
    # 新手提示
    st.info("""
    💡 **新手入门提示**：选择您的零件类型和功能部位，系统将自动推荐合适的形位公差等级。  
    推荐结果基于 GB/T 1184-1996《形状和位置公差 未注公差值》国家标准。
    """)
    
    # ==================== 输入选择区域 ====================
    st.markdown("### 📋 零件信息选择")
    
    # 第一行：零件类型和功能
    row1_col1, row1_col2 = st.columns([1, 2])
    
    with row1_col1:
        # 零件类型选择（带图标）
        part_type = st.selectbox(
            "🏭 零件类型",
            options=list(GEOMETRIC_TOLERANCE_RECOMMENDATIONS.keys()),
            index=0,
            help="选择您要设计的零件类型"
        )
    
    with row1_col2:
        # 根据零件类型动态填充功能选项
        if part_type in GEOMETRIC_TOLERANCE_RECOMMENDATIONS:
            functions = list(GEOMETRIC_TOLERANCE_RECOMMENDATIONS[part_type].keys())
        else:
            functions = []
        part_function = st.selectbox(
            "⚙️ 功能部位",
            options=functions,
            index=0 if functions else None,
            help="选择零件的具体功能部位"
        )
    
    # 第二行：精度等级和参数
    row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1.5])
    
    with row2_col1:
        precision_level = st.selectbox(
            "🎯 精度要求",
            options=["一般（常规机械）", "较高（精密机械）", "很高（高精度设备）"],
            index=0,
            help="根据设备精度要求选择"
        )
    
    with row2_col2:
        param_value = st.number_input(
            "📏 主参数 (mm)",
            value=50.0,
            min_value=0.1,
            max_value=5000.0,
            step=1.0,
            help="零件的主要尺寸（直径、长度等），用于查询公差值"
        )
    
    with row2_col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        query_clicked = st.button(
            "🔍 获取形位公差推荐",
            type="primary",
            use_container_width=True,
            help="点击获取推荐结果"
        )
    
    # ==================== 推荐结果展示 ====================
    if query_clicked:
        if not functions:
            st.warning(f"⚠️ 未找到 '{part_type}' 的推荐数据")
            return
        
        recommendations = GEOMETRIC_TOLERANCE_RECOMMENDATIONS[part_type].get(part_function, [])
        if not recommendations:
            st.warning(f"⚠️ 未找到 '{part_type} - {part_function}' 的推荐数据")
            return
        
        # 精度等级调整映射
        grade_adjust = {"一般（常规机械）": 0, "较高（精密机械）": -1, "很高（高精度设备）": -2}
        adjust = grade_adjust.get(precision_level, 0)
        
        # 统计信息
        st.markdown("---")
        st.markdown(f"### 📊 推荐结果 - {part_type}：{part_function}")
        
        # 显示摘要信息
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        total_items = len(recommendations)
        shape_items = len([r for r in recommendations if r.get("item") in ["圆度", "圆柱度", "直线度", "平面度"]])
        position_items = total_items - shape_items
        
        summary_col1.metric("推荐项目数", f"{total_items} 项")
        summary_col2.metric("形状公差", f"{shape_items} 项")
        summary_col3.metric("位置公差", f"{position_items} 项")
        
        st.markdown("---")
        
        # 逐项显示推荐结果
        for idx, rec in enumerate(recommendations):
            item_name = rec["item"]
            reason = rec.get("reason", "")
            application = rec.get("application", "")
            standard_ref = rec.get("standard_ref", "GB/T 1184")
            base_grade_min, base_grade_max = rec["grade_range"]
            
            # 根据精度等级调整推荐等级范围
            adj_grade_min = max(1, base_grade_min + adjust)
            adj_grade_max = max(1, base_grade_max + adjust)
            
            # 查询公差值（取中间等级）
            mid_grade = (adj_grade_min + adj_grade_max) // 2
            tol_value = lookup_geo_tolerance(item_name, mid_grade, param_value)
            
            # 判断公差类型
            is_shape_tol = item_name in ["圆度", "圆柱度", "直线度", "平面度"]
            tol_type_badge = "🔵 形状公差" if is_shape_tol else "🟠 位置公差"
            
            # 精度等级说明
            grade_desc = ""
            if adj_grade_min <= 5:
                grade_desc = "精密级"
            elif adj_grade_min <= 7:
                grade_desc = "中等精度"
            else:
                grade_desc = "一般精度"
            
            # 创建卡片式布局 - 使用字符串拼接避免花括号冲突
            with st.container():
                # 卡片头部
                header_html = (
                    '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                    'padding: 12px 16px; border-radius: 8px 8px 0 0; margin-top: 10px;">'
                    '<div style="display: flex; justify-content: space-between; align-items: center;">'
                    '<span style="color: white; font-size: 18px; font-weight: bold;">' +
                    str(idx + 1) + '. ' + str(item_name) + '</span>'
                    '<span style="background: rgba(255,255,255,0.2); padding: 4px 12px; '
                    'border-radius: 12px; color: white; font-size: 12px;">' +
                    str(tol_type_badge) + '</span></div></div>'
                )
                st.markdown(header_html, unsafe_allow_html=True)
                
                # 卡片主体 - 使用字符串拼接
                tol_display_str = str(tol_value) if tol_value else "—"
                param_info_str = "@ " + str(param_value) + "mm" if tol_value else "超出查询范围"
                
                # 构建主体HTML
                body_html = (
                    '<div style="background: #f8f9fa; padding: 16px; border-radius: 0 0 8px 8px; '
                    'border: 1px solid #e0e0e0; border-top: none;">'
                    '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">'
                    '<div style="background: white; padding: 12px; border-radius: 6px; '
                    'border-left: 4px solid #667eea;">'
                    '<div style="color: #666; font-size: 12px; margin-bottom: 4px;">📌 推荐等级</div>'
                    '<div style="font-size: 24px; font-weight: bold; color: #333;">' +
                    str(adj_grade_min) + ' ~ ' + str(adj_grade_max) + ' 级</div>'
                    '<div style="color: #888; font-size: 11px;">' + str(grade_desc) + '</div></div>'
                    '<div style="background: white; padding: 12px; border-radius: 6px; '
                    'border-left: 4px solid #48bb78;">'
                    '<div style="color: #666; font-size: 12px; margin-bottom: 4px;">📏 公差值（参考）</div>'
                    '<div style="font-size: 24px; font-weight: bold; color: #333;">' +
                    tol_display_str + ' μm</div>'
                    '<div style="color: #888; font-size: 11px;">' + param_info_str + '</div></div></div>'
                    '<div style="background: white; padding: 12px; border-radius: 6px; margin-top: 12px; '
                    'border-left: 4px solid #f6ad55;">'
                    '<div style="color: #666; font-size: 12px; margin-bottom: 6px;">💡 为什么推荐？</div>'
                    '<div style="color: #444; font-size: 13px; line-height: 1.5;">' + str(reason) + '</div></div>'
                )
                
                # 添加典型应用（如果有）
                if application:
                    body_html += (
                        '<div style="background: white; padding: 12px; border-radius: 6px; margin-top: 12px; '
                        'border-left: 4px solid #4299e1;">'
                        '<div style="color: #666; font-size: 12px; margin-bottom: 6px;">🔧 典型应用</div>'
                        '<div style="color: #444; font-size: 13px; line-height: 1.5;">' + str(application) + '</div></div>'
                    )
                
                # 添加标注建议
                body_html += (
                    '<div style="background: #fff3cd; padding: 10px 12px; border-radius: 6px; margin-top: 12px;">'
                    '<div style="color: #856404; font-size: 12px;">'
                    '<b>📝 标注建议：</b>在零件图上标注 '
                    '<b>' + str(item_name) + '</b> 公差，等级选用 <b>' + str(adj_grade_min) + '~' + str(adj_grade_max) + '级</b>，'
                    '基准标注 <b>📍 A</b>（根据具体位置确定基准要素）</div></div></div>'
                )
                
                st.markdown(body_html, unsafe_allow_html=True)
                
                # 标注示例图
                if tol_value is not None:
                    annotation_svg = generate_gdandt_annotation_svg(
                        item_name, tol_value, mid_grade, param_value
                    )
                    st.markdown(annotation_svg, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # 实用提示
        st.markdown("### 💡 实用提示")
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown("""
            **📋 形位公差等级选用原则：**
            
            | 等级范围 | 应用场合 |
            |---------|---------|
            | 1~2级 | 精密量块、量规、精密机床主轴 |
            | 3~4级 | 精密机床、通用机械重要部位 |
            | 5~7级 | 一般机械的常用配合部位 |
            | 8~9级 | 非配合尺寸、粗糙加工表面 |
            | 10~12级 | 自由尺寸、毛坯件 |
            """)
        
        with tips_col2:
            st.markdown("""
            **⚠️ 常见错误避免：**
            
            1. **基准选择错误**：位置公差必须指定基准，基准要素应是重要的定位或支撑表面
            
            2. **等级过高**：形位公差等级越高加工成本越大，应在满足功能的前提下选用较低的等级
            
            3. **忽略未注公差**：未注形位公差应按 GB/T 1184-K（中等）等级执行
            
            4. **与尺寸公差不协调**：形位公差通常不应大于相应尺寸公差值
            """)
    
    # ==================== 知识卡片 ====================
    st.markdown("### 📚 形位公差知识速查")
    
    knowledge_col1, knowledge_col2, knowledge_col3 = st.columns(3)
    
    with knowledge_col1:
        with st.expander("🔵 形状公差", expanded=False):
            st.markdown("""
            **形状公差** 控制单一要素的形状误差，不涉及基准。
            
            | 项目 | 符号 | 是否需要基准 |
            |-----|------|------------|
            | 直线度 | — | ❌ 否 |
            | 平面度 | ▱ | ❌ 否 |
            | 圆度 | ○ | ❌ 否 |
            | 圆柱度 | ⌭ | ❌ 否 |
            """)
    
    with knowledge_col2:
        with st.expander("🟠 位置公差", expanded=False):
            st.markdown("""
            **位置公差** 控制关联要素对基准的位置误差。
            
            | 项目 | 符号 | 是否需要基准 |
            |-----|------|------------|
            | 平行度 | ∥ | ✅ 是 |
            | 垂直度 | ⊥ | ✅ 是 |
            | 倾斜度 | ∠ | ✅ 是 |
            | 同轴度 | ◎ | ✅ 是 |
            | 对称度 | ⌢ | ✅ 是 |
            | 位置度 | ⌖ | ✅ 是 |
            """)
    
    with knowledge_col3:
        with st.expander("🟣 跳动公差", expanded=False):
            st.markdown("""
            **跳动公差** 是综合公差，测量方便。
            
            | 项目 | 符号 | 是否需要基准 |
            |-----|------|------------|
            | 圆跳动 | ↗ | ✅ 是 |
            | 全跳动 | ⇗ | ✅ 是 |
            
            **特点**：圆跳动可综合反映圆度、同轴度误差；测量简单，是生产中最常用的检测指标。
            """)
    
    # ==================== 手动查询 ====================
    st.markdown("---")
    with st.expander("🔧 手动查询形位公差值", expanded=False):
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


