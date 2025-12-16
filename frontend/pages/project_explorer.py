# frontend/pages/project_explorer.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

API_BASE = "http://localhost:8000/api/v1"

# 预定义的知名开源项目
FAMOUS_PROJECTS = {
    "Apache": [
        "apache/iotdb",
        "apache/kafka",
        "apache/spark",
        "apache/hadoop"
    ],
    "Google": [
        "kubernetes/kubernetes",
        "tensorflow/tensorflow",
        "golang/go",
        "google/jax"
    ],
    "Microsoft": [
        "microsoft/vscode",
        "microsoft/TypeScript",
        "dotnet/core",
        "microsoft/PowerToys"
    ],
    "Meta": [
        "facebook/react",
        "facebook/react-native",
        "pytorch/pytorch"
    ],
    "其他热门项目": [
        "X-lab2017/open-digger",
        "easy-graph/Easy-Graph",
        "tiangolo/fastapi",
        "pallets/flask"
    ]
}

def show_project_explorer():
    """显示项目探索页面"""
    st.header("项目探索")
    
    # 隐藏"Made with Streamlit"标识
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # 初始化 session state
    if 'selected_project' not in st.session_state:
        st.session_state.selected_project = FAMOUS_PROJECTS["Apache"][0]
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "tab1"
    if 'manual_input_value' not in st.session_state:
        st.session_state.manual_input_value = ""

    # 项目选择区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("选择项目")
        
        # 使用选项卡组织项目选择方式
        tab1, tab2 = st.tabs(["选择已有项目", "手动输入项目"])
        
        with tab1:
            # 分类选择项目
            selected_category = st.selectbox("选择项目分类", list(FAMOUS_PROJECTS.keys()))
            selected_in_tab1 = st.selectbox("选择项目", FAMOUS_PROJECTS[selected_category])
            # 更新 session state 中的项目选择
            st.session_state.selected_project = selected_in_tab1
            # 更新当前激活的标签页
            st.session_state.active_tab = "tab1"
            
        with tab2:
            # 手动输入项目
            manual_input = st.text_input("输入项目（格式：owner/repo）", 
                                       value=st.session_state.manual_input_value,
                                       placeholder="例如：apache/iotdb",
                                       key="manual_project_input")
            # 更新 session state 中的手动输入值
            st.session_state.manual_input_value = manual_input
            # 如果用户在tab2中输入了项目，则更新 session state
            if manual_input:
                st.session_state.selected_project = manual_input
            # 更新当前激活的标签页
            st.session_state.active_tab = "tab2"
            
    with col2:
        st.subheader("操作")
        analyze_btn = st.button("🔍 分析项目", type="primary", use_container_width=True)
        st.caption("点击按钮开始分析所选项目")
        
        # 显示当前选中的项目
        if 'selected_project' in st.session_state and st.session_state.selected_project:
            st.info(f"当前选中项目：\n\n**{st.session_state.selected_project}**")
    
    # 项目分析结果显示区域
    if analyze_btn and 'selected_project' in st.session_state and st.session_state.selected_project:
        with st.spinner(f"正在分析项目 {st.session_state.selected_project}..."):
            try:
                owner, repo = st.session_state.selected_project.split('/')
                # 获取项目分析数据
                response = requests.get(f"{API_BASE}/projects/{owner}/{repo}", timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        display_project_analysis(data["data"], owner, repo)
                    else:
                        st.error("项目分析失败，请稍后重试")
                else:
                    st.error("无法获取项目数据，请检查项目名称是否正确")
            except ValueError:
                st.error("项目名称格式不正确，请使用 'owner/repo' 格式")
            except Exception as e:
                st.error(f"分析过程中出现错误: {str(e)}")
    elif analyze_btn:
        st.warning("请先选择或输入一个项目")

# 其余函数保持不变...
def display_project_analysis(data, owner, repo):
    """展示项目分析结果"""
    st.success(f"✅ 成功分析项目 {owner}/{repo}")
    
    # 基本信息展示
    basic_info = data.get("basic_info", {})
    st.subheader(f"📋 项目基本信息 - {basic_info.get('full_name', '')}")
    
    col1, col2, col3, col4 = st.columns(4)
    activity_score = data.get("activity", {}).get("score", 0)
    contributor_count = data.get("community", {}).get("total_contributors", 0)
    newbie_score = data.get("newbie_friendly_score", 0)
    
    col1.metric("📈 活跃度分数", activity_score, help="基于近期活动计算的项目活跃程度")
    col2.metric("👥 贡献者数量", contributor_count, help="项目历史贡献者总数")
    col3.metric("👶 新手友好度", f"{newbie_score}%", help="项目对新贡献者的友好程度")
    col4.metric("📁 平台", basic_info.get("platform", "github").title(), help="项目托管平台")
    
    # 创建多标签页展示详细信息
    tab1, tab2, tab3, tab4 = st.tabs(["📊 活跃度分析", "👥 社区分析", "🐛 问题分析", "💡 贡献建议"])
    
    with tab1:
        display_activity_analysis(data.get("activity", {}))
    
    with tab2:
        display_community_analysis(data.get("community", {}))
    
    with tab3:
        display_issue_analysis(data.get("issues", {}))
    
    with tab4:
        display_contribution_recommendations(owner, repo)

def display_activity_analysis(activity_data):
    """展示活跃度分析"""
    st.subheader("项目活跃度分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        score = activity_data.get("score", 0)
        trend = activity_data.get("trend", "unknown")
        
        # 活跃度评分仪表盘
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "活跃度评分", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [None, 1000], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 300], 'color': 'lightcoral'},
                    {'range': [300, 700], 'color': 'gold'},
                    {'range': [700, 1000], 'color': 'lightgreen'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 800}}))
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 趋势说明
        trend_emojis = {"increasing": "↗️", "decreasing": "↘️", "stable": "➡️", "unknown": "❓"}
        trend_text = {"increasing": "上升", "decreasing": "下降", "stable": "稳定", "unknown": "未知"}
        
        st.metric("趋势", f"{trend_emojis.get(trend, '❓')} {trend_text.get(trend, '未知')}")
        st.caption("基于最近几个月的数据计算得出")
        
        # 活跃度描述
        if score > 800:
            st.success("项目非常活跃，持续有大量更新")
        elif score > 500:
            st.info("项目较为活跃，定期有更新")
        elif score > 200:
            st.warning("项目活跃度一般，更新频率较低")
        else:
            st.error("项目活跃度较低，可能已经停止维护")
    
    # 活跃度趋势图
    recent_months = activity_data.get("recent_months", [])
    if recent_months:
        df = pd.DataFrame(recent_months)
        fig = px.line(df, x="month", y="value", title="近6个月活跃度趋势")
        fig.update_layout(xaxis_title="月份", yaxis_title="活跃度")
        st.plotly_chart(fig, use_container_width=True)

def display_community_analysis(community_data):
    """展示社区分析"""
    st.subheader("社区健康度分析")
    
    col1, col2, col3 = st.columns(3)
    
    total_contributors = community_data.get("total_contributors", 0)
    active_contributors = community_data.get("active_contributors", 0)
    bus_factor = community_data.get("bus_factor", 0)
    
    col1.metric("总贡献者数", total_contributors)
    col2.metric("活跃贡献者数", active_contributors)
    col3.metric("Bus Factor", bus_factor, help="项目风险指标，数值越低风险越高")
    
    # Bus Factor 解释
    if bus_factor <= 2:
        st.error("⚠️ 项目 Bus Factor 较低，存在单点故障风险")
    elif bus_factor <= 5:
        st.warning("ℹ️ 项目 Bus Factor 中等，建议关注核心贡献者")
    else:
        st.success("✅ 项目 Bus Factor 良好，社区分布较为健康")
    
    # 关键贡献者
    key_contributors = community_data.get("key_contributors", [])
    if key_contributors:
        st.subheader("关键贡献者 Top 5")
        df = pd.DataFrame(key_contributors)
        st.dataframe(df.style.background_gradient(cmap='Blues'), use_container_width=True)
        
        # 贡献者可视化
        fig = px.bar(df, x="name", y="contributions", title="关键贡献者贡献量")
        fig.update_layout(xaxis_title="贡献者", yaxis_title="贡献次数")
        st.plotly_chart(fig, use_container_width=True)

def display_issue_analysis(issues_data):
    """展示问题分析"""
    st.subheader("问题处理分析")
    
    col1, col2, col3 = st.columns(3)
    
    new_issues = issues_data.get("new_issues", 0)
    closed_issues = issues_data.get("closed_issues", 0)
    resolution_efficiency = issues_data.get("resolution_efficiency", 0)
    avg_response_time = issues_data.get("avg_response_time", 0)
    
    col1.metric("新增问题数", new_issues)
    col2.metric("已关闭问题数", closed_issues)
    col3.metric("问题解决效率", f"{resolution_efficiency}%", help="已关闭问题占新增问题的比例")
    
    # 响应时间
    st.metric("平均响应时间", f"{avg_response_time} 小时")
    
    # 问题处理状态评价
    if resolution_efficiency >= 90:
        st.success("✅ 问题解决效率很高，社区响应积极")
    elif resolution_efficiency >= 70:
        st.info("ℹ️ 问题解决效率良好")
    else:
        st.warning("⚠️ 问题解决效率有待提升")
        
    if avg_response_time <= 24:
        st.success("✅ 社区响应速度很快")
    elif avg_response_time <= 72:
        st.info("ℹ️ 社区响应速度适中")
    else:
        st.warning("⚠️ 社区响应较慢")

def display_contribution_recommendations(owner, repo):
    """展示贡献建议"""
    st.subheader("个性化贡献建议")
    
    try:
        # 获取贡献建议
        response = requests.get(f"{API_BASE}/projects/{owner}/{repo}/recommendations", timeout=10)
        if response.status_code == 200:
            rec_data = response.json()
            if rec_data.get("success"):
                recommendations = rec_data["data"].get("recommendations", [])
                
                if recommendations:
                    # 按优先级分组显示
                    priority_order = ["high", "medium", "low"]
                    priority_names = {"high": "高优先级", "medium": "中优先级", "low": "低优先级"}
                    priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    
                    for priority in priority_order:
                        priority_recs = [r for r in recommendations if r["priority"] == priority]
                        if priority_recs:
                            st.markdown(f"#### {priority_colors[priority]} {priority_names[priority]}建议")
                            for rec in priority_recs:
                                with st.expander(rec["title"]):
                                    st.write(rec["description"])
                                    st.caption(f"类型: {rec['type']}")
                else:
                    st.info("暂无具体的贡献建议")
            else:
                st.error("获取贡献建议失败")
        else:
            st.error("无法获取贡献建议")
    except Exception as e:
        st.error(f"获取贡献建议时出错: {e}")
    
    # 通用贡献提示
    st.subheader("通用贡献指南")
    st.markdown("""
    1. **阅读贡献指南** - 在开始之前，请务必阅读项目的 CONTRIBUTING.md 文件
    2. **从小事做起** - 可以从修复拼写错误、改进文档开始
    3. **参与讨论** - 在问题或PR下发表建设性意见也是重要贡献
    4. **遵守规范** - 遵循项目的代码风格和提交规范
    5. **保持耐心** - 开源社区的响应可能需要一些时间
    """)