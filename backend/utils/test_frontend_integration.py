# backend/utils/test_frontend_integration.py
import requests
import json

def test_frontend_integration():
    """测试前端与后端的集成"""
    api_base = "http://localhost:8000/api/v1"
    
    print("🔍 测试前端与后端集成...")
    print("=" * 50)
    
    # 模拟前端请求模式
    test_projects = [
        ("apache", "iotdb"),
        ("X-lab2017", "open-digger"),
        ("easy-graph", "Easy-Graph")
    ]
    
    print("模拟前端项目探索页面请求...")
    
    # 1. 测试项目列表数据获取 (类似前端project_explorer.py)
    projects_data = []
    for project_path in test_projects:
        owner, repo = project_path
        try:
            response = requests.get(f"{api_base}/projects/{owner}/{repo}/metrics", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    metrics_data = data["data"]
                    project_info = {
                        "name": f"{owner}/{repo}",
                        "activity_score": metrics_data.get("activity_score", 0),
                        "contributors": metrics_data.get("community_health", {}).get("total_contributors", 0),
                        "newbie_friendly": metrics_data.get("newbie_friendly_score", 0)
                    }
                    projects_data.append(project_info)
                    print(f"   ✅ {owner}/{repo}: 数据获取成功")
                else:
                    print(f"   ⚠️  {owner}/{repo}: API返回失败")
            else:
                print(f"   ⚠️  {owner}/{repo}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {owner}/{repo}: 请求异常 - {e}")
    
    print(f"\n获取到 {len(projects_data)} 个项目的数据")
    if projects_data:
        for project in projects_data:
            print(f"   - {project['name']}: 活跃度{project['activity_score']}, 贡献者{project['contributors']}人, 友好度{project['newbie_friendly']}")
    
    # 2. 测试项目详情数据获取
    if projects_data:
        print("\n模拟前端项目详情页面请求...")
        sample_project = projects_data[0]  # 测试第一个项目
        owner, repo = sample_project["name"].split("/")
        
        # 获取完整分析报告
        try:
            response = requests.get(f"{api_base}/projects/{owner}/{repo}", timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    analysis_data = data["data"]
                    print("   ✅ 项目详情获取成功")
                    print(f"      基础信息: {analysis_data.get('basic_info', {})}")
                    print(f"      活跃度分析: {analysis_data.get('activity', {})}")
                    print(f"      社区分析: {analysis_data.get('community', {})}")
                    print(f"      问题分析: {analysis_data.get('issues', {})}")
                else:
                    print("   ⚠️  项目详情API返回失败")
            else:
                print(f"   ⚠️  项目详情HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 项目详情请求异常: {e}")
        
        # 获取贡献建议
        try:
            response = requests.get(f"{api_base}/projects/{owner}/{repo}/recommendations", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    recommendations = data["data"].get("recommendations", [])
                    print("   ✅ 贡献建议获取成功")
                    print(f"      建议数量: {len(recommendations)}")
                    for rec in recommendations[:2]:  # 显示前2个建议
                        print(f"      - [{rec.get('priority', '')}] {rec.get('title', '')}")
                else:
                    print("   ⚠️  贡献建议API返回失败")
            else:
                print(f"   ⚠️  贡献建议HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 贡献建议请求异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 前端集成测试完成!")

if __name__ == "__main__":
    test_frontend_integration()