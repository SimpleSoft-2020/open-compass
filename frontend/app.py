import streamlit as st
import requests
import pandas as pd

# 应用配置
st.set_page_config(
    page_title="开源罗盘",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用状态管理
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# API配置
API_BASE = "http://localhost:8000/api/v1"

def init_app():
    """初始化应用"""
    # 测试API连接
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            st.session_state.api_available = True
            st.session_state.api_status = response.json()
        else:
            st.session_state.api_available = False
    except:
        st.session_state.api_available = False
    
    st.session_state.initialized = True

def main():
    """主应用"""
    # 初始化
    if not st.session_state.initialized:
        init_app()
    
    # 标题栏
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🧭 开源罗盘")
        st.caption("开源贡献者智能导航系统 - 开发中")
    
    # 状态栏
    with st.sidebar:
        st.header("系统状态")
        
        # API状态
        if st.session_state.api_available:
            st.success("✅ API服务正常")
            st.json(st.session_state.api_status)
        else:
            st.error("❌ API服务不可用")
            st.info("请确保后端服务已启动")
        
        # 快速导航
        st.divider()
        st.header("快速导航")
        nav_options = [
            "🏠 首页",
            "🔍 项目探索", 
            "🎯 任务推荐",
            "📊 我的成长",
            "⚙️ 系统设置"
        ]
        nav_choice = st.radio("导航", nav_options)
        
        # 项目选择
        st.divider()
        st.header("关注项目")
        projects = ["apache/iotdb", "X-lab2017/open-digger", "easy-graph/Easy-Graph"]
        selected_projects = st.multiselect("选择项目", projects, default=projects[0])
        st.session_state.selected_projects = selected_projects
    
    # 主内容区
    if nav_choice == "🏠 首页":
        show_home_page()
    elif nav_choice == "🔍 项目探索":
        show_project_explorer()
    elif nav_choice == "🎯 任务推荐":
        show_task_recommendation()
    elif nav_choice == "📊 我的成长":
        show_growth_tracking()
    elif nav_choice == "⚙️ 系统设置":
        show_settings()

def show_home_page():
    """显示首页"""
    st.header("欢迎使用开源罗盘")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🌟 项目介绍
        **开源罗盘**是一个智能化的开源贡献者导航系统，旨在帮助：
        
        - 🚀 **开源新人**：快速找到合适的贡献起点
        - 📈 **成长中贡献者**：规划清晰的成长路径  
        - 🛠️ **项目维护者**：高效管理社区和发现人才
        
        ### 🔧 当前状态
        - ✅ 项目框架已搭建
        - 🔄 核心功能开发中
        - 📚 数据连接准备中
        
        ### 🎯 即将实现
        1. GitHub项目数据分析
        2. 智能任务推荐算法
        3. 贡献者成长可视化
        4. 社区健康度监控
        """)
    
    with col2:
        # 项目统计卡片
        st.metric("关注项目", len(st.session_state.get('selected_projects', [])))
        st.metric("API状态", "正常" if st.session_state.api_available else "异常")
        st.metric("数据源", "GitHub API")
        
        # 快速开始
        st.divider()
        st.subheader("快速开始")
        
        if st.button("🔍 探索项目", type="primary"):
            st.switch_page("frontend/pages/explorer.py")
        
        if st.button("🎯 获取推荐"):
            st.info("功能开发中...")
        
        if st.button("📊 查看示例"):
            show_example_data()

def show_project_explorer():
    """显示项目探索页面"""
    st.header("项目探索")
    st.info("此功能正在开发中，即将上线...")
    
    # 占位数据
    projects = [
        {"name": "Apache IoTDB", "stars": 3500, "issues": 120, "newbie_friendly": 85},
        {"name": "OpenDigger", "stars": 1200, "issues": 45, "newbie_friendly": 92},
        {"name": "EasyGraph", "stars": 800, "issues": 32, "newbie_friendly": 78},
    ]
    
    df = pd.DataFrame(projects)
    st.dataframe(df, use_container_width=True)
    
    # 项目选择器
    selected = st.selectbox("选择项目查看详情", df["name"].tolist())
    
    if selected:
        st.subheader(f"{selected} 详情")
        col1, col2, col3 = st.columns(3)
        col1.metric("⭐ Stars", df[df["name"] == selected]["stars"].values[0])
        col2.metric("🐛 Issues", df[df["name"] == selected]["issues"].values[0])
        col3.metric("👶 新手友好度", f"{df[df['name'] == selected]['newbie_friendly'].values[0]}%")

def show_task_recommendation():
    """显示任务推荐页面"""
    st.header("任务推荐")
    st.warning("推荐引擎正在开发中...")
    
    # 用户技能输入
    with st.form("skill_form"):
        st.subheader("您的技能")
        col1, col2 = st.columns(2)
        
        with col1:
            languages = st.multiselect(
                "编程语言",
                ["Python", "Java", "JavaScript", "C++", "Go", "Rust"],
                default=["Python"]
            )
            
        with col2:
            skill_level = st.select_slider(
                "技能水平",
                options=["初学者", "中级", "高级", "专家"]
            )
        
        interests = st.multiselect(
            "兴趣领域",
            ["数据分析", "机器学习", "Web开发", "系统编程", "文档", "测试"]
        )
        
        submitted = st.form_submit_button("获取推荐", type="primary")
    
    if submitted:
        st.success(f"已收到您的信息：{len(languages)}种语言，{skill_level}水平")
        st.info("推荐算法正在训练中，请稍候...")
        
        # 占位推荐
        st.subheader("为您推荐")
        recommendations = [
            {"任务": "修复文档错别字", "项目": "IoTDB", "匹配度": 92, "预估时间": "1小时"},
            {"任务": "添加单元测试", "项目": "OpenDigger", "匹配度": 85, "预估时间": "3小时"},
            {"任务": "优化代码注释", "项目": "EasyGraph", "匹配度": 78, "预估时间": "2小时"},
        ]
        st.dataframe(pd.DataFrame(recommendations), use_container_width=True)

def show_growth_tracking():
    """显示成长追踪页面"""
    st.header("我的成长")
    st.info("成长追踪功能即将上线...")
    
    # 示例图表
    chart_data = pd.DataFrame({
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '贡献数': [2, 5, 8, 12, 15, 18],
        '技能增长': [30, 45, 60, 70, 85, 95]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("贡献趋势")
        st.line_chart(chart_data, x='月份', y='贡献数')
    
    with col2:
        st.subheader("技能成长")
        st.area_chart(chart_data, x='月份', y='技能增长')
    
    # 成就徽章
    st.subheader("成就徽章")
    badges = ["🏅 首次贡献", "🎯 连续贡献", "🌟 代码审查", "📚 文档大师", "🔧 问题解决"]
    cols = st.columns(5)
    for col, badge in zip(cols, badges):
        with col:
            st.markdown(f"### {badge}")
            st.progress(75 if badge == "🏅 首次贡献" else 25)

def show_settings():
    """显示设置页面"""
    st.header("系统设置")
    
    tab1, tab2, tab3 = st.tabs(["API配置", "界面设置", "数据管理"])
    
    with tab1:
        st.subheader("API配置")
        github_token = st.text_input("GitHub Token (可选)", type="password")
        api_endpoint = st.text_input("API端点", value="http://localhost:8000")
        
        if st.button("测试连接"):
            try:
                response = requests.get(f"{api_endpoint}/health")
                if response.status_code == 200:
                    st.success("✅ 连接成功")
                else:
                    st.error("❌ 连接失败")
            except:
                st.error("❌ 无法连接到API")
        
        if st.button("保存配置", type="primary"):
            st.success("配置已保存")
    
    with tab2:
        st.subheader("界面设置")
        theme = st.selectbox("主题", ["浅色", "深色", "自动"])
        language = st.selectbox("语言", ["中文", "English"])
        st.checkbox("显示开发者工具", value=True)
        
        if st.button("应用设置"):
            st.success("设置已应用")
    
    with tab3:
        st.subheader("数据管理")
        st.info("数据管理功能开发中...")
        
        if st.button("清除缓存数据"):
            st.warning("这将清除所有本地缓存数据")
        
        if st.button("导出我的数据"):
            st.success("数据导出功能开发中...")

def show_example_data():
    """显示示例数据"""
    st.subheader("示例数据")
    
    # 示例贡献者数据
    contributors = pd.DataFrame({
        '姓名': ['Alice', 'Bob', 'Charlie', 'Diana'],
        '贡献数': [45, 28, 67, 32],
        '主要语言': ['Python', 'Java', 'JavaScript', 'Go'],
        '加入时间': ['2023-01', '2023-03', '2022-11', '2023-06']
    })
    
    st.write("### 示例贡献者")
    st.dataframe(contributors, use_container_width=True)
    
    # 示例任务数据
    tasks = pd.DataFrame({
        '任务ID': ['#123', '#124', '#125', '#126'],
        '标题': ['修复文档错误', '添加测试用例', '优化性能', '翻译文档'],
        '难度': ['简单', '中等', '困难', '简单'],
        '预估时间': ['1小时', '3小时', '8小时', '2小时'],
        '匹配度': [95, 87, 65, 92]
    })
    
    st.write("### 示例任务推荐")
    st.dataframe(tasks, use_container_width=True)

if __name__ == "__main__":
    main()