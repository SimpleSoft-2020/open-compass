# frontend/pages/project_explorer.py
import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000/api/v1"

def show_project_explorer():
    """显示项目探索页面"""
    st.header("项目探索")
    
    # 默认关注的项目
    default_projects = ["apache/iotdb", "X-lab2017/open-digger", "easy-graph/Easy-Graph"]
    
    projects_data = []
    for project_path in default_projects:
        owner, repo = project_path.split('/')
        try:
            # 从API获取真实数据
            response = requests.get(f"{API_BASE}/projects/{owner}/{repo}/metrics", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    metrics_data = data["data"]
                    projects_data.append({
                        "name": f"{owner}/{repo}",
                        "activity_score": metrics_data.get("activity_score", 0),
                        "contributors": metrics_data.get("community_health", {}).get("total_contributors", 0),
                        "newbie_friendly": metrics_data.get("newbie_friendly_score", 0)
                    })
                else:
                    # Fallback to mock data
                    projects_data.append(get_mock_project_data(owner, repo))
            else:
                # Fallback to mock data
                projects_data.append(get_mock_project_data(owner, repo))
        except Exception as e:
            # Fallback to mock data on error
            print(f"Error fetching {owner}/{repo}: {e}")
            projects_data.append(get_mock_project_data(owner, repo))
    
    if projects_data:
        df = pd.DataFrame(projects_data)
        st.dataframe(df, use_container_width=True)
        
        # 项目详情查看
        selected = st.selectbox("选择项目查看详情", df["name"].tolist())
        
        if selected:
            owner, repo = selected.split('/')
            show_project_detail(owner, repo)
    else:
        st.warning("暂时无法获取项目数据，请稍后再试")
        # 显示模拟数据
        show_mock_project_data()

def get_mock_project_data(owner: str, repo: str) -> dict:
    """获取模拟项目数据"""
    mock_data = {
        "apache/iotdb": {"name": "apache/iotdb", "activity_score": 850, "contributors": 45, "newbie_friendly": 85},
        "X-lab2017/open-digger": {"name": "X-lab2017/open-digger", "activity_score": 720, "contributors": 28, "newbie_friendly": 92},
        "easy-graph/Easy-Graph": {"name": "easy-graph/Easy-Graph", "activity_score": 580, "contributors": 18, "newbie_friendly": 78}
    }
    return mock_data.get(f"{owner}/{repo}", {"name": f"{owner}/{repo}", "activity_score": 0, "contributors": 0, "newbie_friendly": 50})

def show_project_detail(owner: str, repo: str):
    """显示项目详情"""
    st.subheader(f"{owner}/{repo} 详情")
    
    try:
        # 获取完整分析报告
        response = requests.get(f"{API_BASE}/projects/{owner}/{repo}", timeout=10)
        if response.status_code == 200:
            project_data = response.json()
            if project_data.get("success"):
                data = project_data["data"]
                
                # 显示基础指标
                col1, col2, col3 = st.columns(3)
                col1.metric("📈 活跃度分数", data.get("activity", {}).get("score", 0))
                col2.metric("👥 贡献者数量", data.get("community", {}).get("total_contributors", 0))
                col3.metric("👶 新手友好度", data.get("newbie_friendly_score", 0))
                
                # 显示趋势图
                activity_history = data.get("activity", {}).get("recent_months", [])
                if activity_history:
                    chart_data = pd.DataFrame(activity_history)
                    st.subheader("活跃度趋势")
                    st.line_chart(chart_data.set_index('month')['value'])
                
                # 显示关键贡献者
                key_contributors = data.get("community", {}).get("key_contributors", [])
                if key_contributors:
                    st.subheader("关键贡献者")
                    contrib_df = pd.DataFrame(key_contributors)
                    st.dataframe(contrib_df, use_container_width=True)
                
                # 获取并显示贡献建议
                show_project_recommendations(owner, repo)
            else:
                st.error("无法获取项目详情")
        else:
            st.error("无法获取项目详情")
    except Exception as e:
        st.error(f"获取项目详情时出错: {e}")

def show_project_recommendations(owner: str, repo: str):
    """显示项目贡献建议"""
    try:
        response = requests.get(f"{API_BASE}/projects/{owner}/{repo}/recommendations", timeout=10)
        if response.status_code == 200:
            rec_data = response.json()
            if rec_data.get("success"):
                recommendations = rec_data["data"].get("recommendations", [])
                if recommendations:
                    st.subheader("贡献建议")
                    for rec in recommendations:
                        priority_emoji = {
                            "high": "🔴",
                            "medium": "🟡",
                            "low": "🟢"
                        }
                        st.markdown(f"{priority_emoji.get(rec['priority'], '⚪')} **{rec['title']}**")
                        st.markdown(f"*{rec['description']}*")
                        st.divider()
            else:
                st.info("暂无贡献建议")
        else:
            st.info("暂无贡献建议")
    except Exception as e:
        st.info("暂无贡献建议")

def show_mock_project_data():
    """显示模拟项目数据"""
    st.info("显示模拟数据")
    # 占位数据
    projects = [
        {"name": "Apache IoTDB", "activity_score": 850, "contributors": 45, "newbie_friendly": 85},
        {"name": "OpenDigger", "activity_score": 720, "contributors": 28, "newbie_friendly": 92},
        {"name": "EasyGraph", "activity_score": 580, "contributors": 18, "newbie_friendly": 78},
    ]
    
    df = pd.DataFrame(projects)
    st.dataframe(df, use_container_width=True)