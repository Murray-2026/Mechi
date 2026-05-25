# -*- coding: utf-8 -*-
"""
尺寸链计算模块
"""

import streamlit as st
import pandas as pd
from io import BytesIO

from modules.utils import (
    calculate_dimension_chain,
    generate_dimension_chain_svg,
)


def generate_html_report(components, result):
    """生成完整的HTML计算报告"""
    # 组成环表格HTML
    ring_rows = ""
    for c in result["contributions"]:
        ring_rows += (
            "<tr>"
            f"<td>{c['name']}</td>"
            f"<td>{'增环' if c['ring_type'] == '增环' else '减环'}</td>"
            f"<td>{c['basic_size']:.3f}</td>"
            f"<td>{c['upper_dev']:+.3f}</td>"
            f"<td>{c['lower_dev']:+.3f}</td>"
            f"<td>{c['tolerance']:.3f}</td>"
            f"<td>{c['contribution']:+.3f}</td>"
            "</tr>"
        )

    # 增环减环汇总
    add_rings = [c for c in result["contributions"] if c["ring_type"] == "增环"]
    sub_rings = [c for c in result["contributions"] if c["ring_type"] == "减环"]
    add_size = sum(c["basic_size"] for c in add_rings)
    sub_size = sum(c["basic_size"] for c in sub_rings)
    add_upper = sum(c["upper_dev"] for c in add_rings)
    add_lower = sum(c["lower_dev"] for c in add_rings)
    sub_upper = sum(c["upper_dev"] for c in sub_rings)
    sub_lower = sum(c["lower_dev"] for c in sub_rings)

    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>尺寸链计算报告</title>
<style>
  body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 40px; color: #333; }}
  h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
  h2 {{ color: #34495e; margin-top: 30px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
  th, td {{ border: 1px solid #ddd; padding: 10px; text-align: center; }}
  th {{ background: #3498db; color: white; }}
  tr:nth-child(even) {{ background: #f8f9fa; }}
  .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
  .metric-box {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
  .metric-box .label {{ font-size: 13px; opacity: 0.9; }}
  .metric-box .value {{ font-size: 24px; font-weight: bold; margin-top: 5px; }}
  .formula {{ background: #ecf0f1; padding: 15px; border-radius: 8px; font-family: monospace; margin: 10px 0; }}
  .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; margin: 10px 0; border-radius: 4px; }}
  .footer {{ margin-top: 40px; text-align: center; color: #7f8c8d; font-size: 12px; }}
  .section {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px 0; }}
</style>
</head>
<body>
  <h1>📏 尺寸链计算报告</h1>
  <p><strong>生成时间：</strong>{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

  <!-- 输入参数 -->
  <div class="section">
    <h2>一、输入参数</h2>
    <table>
      <thead>
        <tr>
          <th>名称</th>
          <th>环类型</th>
          <th>基本尺寸 (mm)</th>
          <th>上偏差 (mm)</th>
          <th>下偏差 (mm)</th>
          <th>最大极限 (mm)</th>
          <th>最小极限 (mm)</th>
        </tr>
      </thead>
      <tbody>
        {''.join(f"<tr>"
          f"<td>{c['name']}</td>"
          f"<td>{c['ring_type']}</td>"
          f"<td>{c['basic_size']:.3f}</td>"
          f"<td>{c['upper_dev']:+.3f}</td>"
          f"<td>{c['lower_dev']:+.3f}</td>"
          f"<td>{c['basic_size']+c['upper_dev']:.3f}</td>"
          f"<td>{c['basic_size']+c['lower_dev']:.3f}</td>"
          f"</tr>" for c in components)}
      </tbody>
    </table>
  </div>

  <!-- 计算方法 -->
  <div class="section">
    <h2>二、计算方法（极值法）</h2>
    <div class="formula">
      <strong>封闭环基本尺寸：</strong><br>
      A₀ = Σ(增环基本尺寸) - Σ(减环基本尺寸)<br>
      = {add_size:.3f} - {sub_size:.3f}<br>
      = <strong>{result['A0']:.3f} mm</strong>
    </div>
    <div class="formula">
      <strong>封闭环上偏差：</strong><br>
      ES₀ = Σ(增环上偏差) - Σ(减环下偏差)<br>
      = {add_upper:+.3f} - ({sub_lower:+.3f})<br>
      = <strong>{result['ES0']:+.3f} mm</strong>
    </div>
    <div class="formula">
      <strong>封闭环下偏差：</strong><br>
      EI₀ = Σ(增环下偏差) - Σ(减环上偏差)<br>
      = {add_lower:+.3f} - ({sub_upper:+.3f})<br>
      = <strong>{result['EI0']:+.3f} mm</strong>
    </div>
    <div class="formula">
      <strong>封闭环公差：</strong><br>
      T₀ = ES₀ - EI₀ = {result['ES0']:+.3f} - ({result['EI0']:+.3f})<br>
      = <strong>{result['T0']:.3f} mm</strong>
    </div>
    <div class="warning">
      <strong>⚠️ 极值法说明：</strong>极值法（worst-case method）考虑所有组成环同时处于极限尺寸的最不利组合，
      保证了100%的零件在装配后一定满足封闭环要求，但可能会导致公差要求过严，增加制造成本。
      当组成环数量较多（>4）时，可考虑采用统计公差法。
    </div>
  </div>

  <!-- 计算结果 -->
  <div class="section">
    <h2>三、计算结果</h2>
    <div class="metric-grid">
      <div class="metric-box">
        <div class="label">封闭环基本尺寸</div>
        <div class="value">{result['A0']:.3f} mm</div>
      </div>
      <div class="metric-box" style="background: linear-gradient(135deg, #11998e, #38ef7d);">
        <div class="label">上偏差 (ES₀)</div>
        <div class="value">{result['ES0']:+.3f} mm</div>
      </div>
      <div class="metric-box" style="background: linear-gradient(135deg, #eb3349, #f45c43);">
        <div class="label">下偏差 (EI₀)</div>
        <div class="value">{result['EI0']:+.3f} mm</div>
      </div>
      <div class="metric-box" style="background: linear-gradient(135deg, #f12711, #f5af19);">
        <div class="label">公差值 (T₀)</div>
        <div class="value">{result['T0']:.3f} mm</div>
      </div>
    </div>
    <table>
      <tr><th>最大极限尺寸</th><td>{result['A0_max']:.3f} mm</td></tr>
      <tr><th>最小极限尺寸</th><td>{result['A0_min']:.3f} mm</td></tr>
      <tr><th>公差等级（参考）</th><td>IT{result.get('it_grade', '—')}</td></tr>
    </table>
  </div>

  <!-- 组成环贡献分析 -->
  <div class="section">
    <h2>四、组成环公差贡献分析</h2>
    <table>
      <thead>
        <tr>
          <th>名称</th>
          <th>环类型</th>
          <th>基本尺寸</th>
          <th>公差</th>
          <th>公差贡献</th>
          <th>贡献占比</th>
        </tr>
      </thead>
      <tbody>
        {''.join(f"<tr>"
          f"<td>{c['name']}</td>"
          f"<td>{c['ring_type']}</td>"
          f"<td>{c['basic_size']:.3f} mm</td>"
          f"<td>{c['tolerance']:.3f} mm</td>"
          f"<td>{c['contribution']:+.3f} mm</td>"
          f"<td>{c['contribution']/result['T0']*100:.1f}%</td>"
          f"</tr>" for c in result["contributions"])}
      </tbody>
    </table>
    <p><strong>💡 分析：</strong>公差贡献最大的组成环是对封闭环精度影响最大的环节，
    在进行工艺能力改进时应优先考虑优化该环的公差。</p>
  </div>

  <!-- 结论与建议 -->
  <div class="section">
    <h2>五、结论与建议</h2>
    <ul>
      <li>封闭环尺寸范围为 <strong>{result['A0_min']:.3f} ~ {result['A0_max']:.3f} mm</strong></li>
      <li>封闭环公差为 <strong>{result['T0']:.3f} mm</strong></li>
      <li>公差贡献最大的组成环是 <strong>{max(result['contributions'], key=lambda x: x['contribution'])['name']}</strong>（贡献 {max(result['contributions'], key=lambda x: x['contribution'])['contribution']/result['T0']*100:.1f}%）</li>
      <li>建议在加工时重点控制该环的尺寸精度</li>
      {f"<li>组成环数量较多（{len(components)}个），可考虑采用统计公差法以获得更宽松的公差分配</li>" if len(components) > 4 else ""}
    </ul>
  </div>

  <div class="footer">
    <p>⚙️ 机械公差助手 | 尺寸链计算报告</p>
    <p>⚠️ 本报告仅供参考，关键设计请以国家标准和设计手册为准</p>
  </div>
</body>
</html>
"""
    return html


def export_to_excel(components, result):
    """导出计算结果到Excel"""
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet1: 输入参数
        input_df = pd.DataFrame([
            {
                "名称": c["name"],
                "环类型": c["ring_type"],
                "基本尺寸(mm)": c["basic_size"],
                "上偏差(mm)": c["upper_dev"],
                "下偏差(mm)": c["lower_dev"],
                "最大极限(mm)": c["basic_size"] + c["upper_dev"],
                "最小极限(mm)": c["basic_size"] + c["lower_dev"],
            }
            for c in components
        ])
        input_df.to_excel(writer, sheet_name="输入参数", index=False)

        # Sheet2: 计算结果
        result_df = pd.DataFrame([
            {"项目": "封闭环基本尺寸", "数值": f"{result['A0']:.3f}", "单位": "mm"},
            {"项目": "上偏差(ES₀)", "数值": f"{result['ES0']:+.3f}", "单位": "mm"},
            {"项目": "下偏差(EI₀)", "数值": f"{result['EI0']:+.3f}", "单位": "mm"},
            {"项目": "公差值(T₀)", "数值": f"{result['T0']:.3f}", "单位": "mm"},
            {"项目": "最大极限尺寸", "数值": f"{result['A0_max']:.3f}", "单位": "mm"},
            {"项目": "最小极限尺寸", "数值": f"{result['A0_min']:.3f}", "单位": "mm"},
        ])
        result_df.to_excel(writer, sheet_name="计算结果", index=False)

        # Sheet3: 组成环贡献
        contrib_df = pd.DataFrame(result["contributions"])
        contrib_df.columns = ["名称", "环类型", "基本尺寸", "上偏差", "下偏差", "公差", "公差贡献"]
        contrib_df["贡献占比(%)"] = contrib_df["公差贡献"].apply(
            lambda x: f"{x/result['T0']*100:.1f}%"
        )
        contrib_df.to_excel(writer, sheet_name="组成环贡献", index=False)

    output.seek(0)
    return output


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

    # 显示尺寸链示意图
    st.markdown("### 尺寸链示意图")
    svg_diagram = generate_dimension_chain_svg(st.session_state.dim_chain_components)
    st.markdown(svg_diagram, unsafe_allow_html=True)
    st.caption("💡 示意图说明：第一个组成环（A1）为总尺寸显示在上方，其余组成环为分段尺寸显示在下方，A₀为封闭环间隙")

    st.markdown("---")

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

        # 保存结果到session_state
        st.session_state.dim_chain_result = result

        # 显示结果
        st.markdown("### 计算结果")
        st.success("尺寸链计算完成！可导出报告或Excel")

        # 4个指标卡片
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("封闭环基本尺寸", f"{result['A0']:.3f} mm")
        col2.metric("上偏差", f"{result['ES0']:+.3f} mm")
        col3.metric("下偏差", f"{result['EI0']:+.3f} mm")
        col4.metric("公差值", f"{result['T0']:.3f} mm")

        # 导出选项
        export_col1, export_col2, export_col3 = st.columns(3)
        with export_col1:
            # 生成HTML报告
            html_report = generate_html_report(components, result)
            st.download_button(
                "📥 下载HTML报告",
                data=html_report.encode("utf-8"),
                file_name="尺寸链计算报告.html",
                mime="text/html",
                use_container_width=True,
            )
        with export_col2:
            # 导出Excel
            excel_data = export_to_excel(components, result)
            st.download_button(
                "📊 导出Excel",
                data=excel_data,
                file_name="尺寸链计算结果.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with export_col3:
            # 复制文本
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
            st.download_button(
                "📋 复制文本",
                data=copy_text,
                file_name="尺寸链计算结果.txt",
                mime="text/plain",
                use_container_width=True,
            )

        # 组成环详情表格
        st.markdown("#### 组成环详情")
        table_data = []
        for c in result["contributions"]:
            pct = c["contribution"] / result["T0"] * 100
            table_data.append({
                "名称": c["name"],
                "环类型": c["ring_type"],
                "基本尺寸(mm)": c["basic_size"],
                "公差(mm)": f"{c['tolerance']:.3f}",
                "公差贡献(mm)": f"{c['contribution']:+.3f}",
                "贡献占比": f"{pct:.1f}%",
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 计算过程
        with st.expander("📝 查看计算过程详解", expanded=False):
            st.code(result["details"], language="text")

    # 底部说明
    st.markdown("---")
    st.caption("💡 **极值法说明**：极值法考虑所有组成环同时处于极限尺寸的最不利组合，保证100%装配合格率。当组成环数量>4时，可考虑采用统计公差法。")
