# backend/utils/test_api.py
import requests
import json

def test_opendigger_api():
    """测试OpenDigger API功能"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🔍 测试OpenDigger API...")
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✅ 健康检查成功: {response.json()}")
    except Exception as e:
        print(f"  ❌ 健康检查失败: {e}")
    
    # 测试项目分析API
    test_projects = [
        ("apache", "iotdb"),
        ("X-lab2017", "open-digger"),
        ("easy-graph", "Easy-Graph")
    ]
    
    for owner, repo in test_projects:
        print(f"\n=== 测试项目: {owner}/{repo} ===")
        
        # 测试综合分析
        try:
            response = requests.get(f"{base_url}/projects/{owner}/{repo}")
            print(f"综合分析: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"  ✅ 综合分析成功")
                    print(f"  🐍 新手友好度: {data['data'].get('newbie_friendly_score', 0)}")
                else:
                    print(f"  ❌ 综合分析失败: {data.get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"  ❌ 综合分析异常: {e}")
        
        # 测试关键指标
        try:
            response = requests.get(f"{base_url}/projects/{owner}/{repo}/metrics")
            print(f"关键指标: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"  ✅ 关键指标获取成功")
                    metrics = data.get("data", {})
                    print(f"  📊 活跃度分数: {metrics.get('activity_score', 0)}")
                    print(f"  👥 贡献者数量: {metrics.get('community_health', {}).get('total_contributors', 0)}")
                else:
                    print(f"  ❌ 关键指标获取失败: {data.get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"  ❌ 关键指标异常: {e}")
        
        # 测试贡献建议
        try:
            response = requests.get(f"{base_url}/projects/{owner}/{repo}/recommendations")
            print(f"贡献建议: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"  ✅ 贡献建议获取成功")
                    recommendations = data.get("data", {}).get("recommendations", [])
                    print(f"  💡 建议数量: {len(recommendations)}")
                    if recommendations:
                        print(f"  🎯 首条建议: {recommendations[0].get('title', '')}")
                else:
                    print(f"  ❌ 贡献建议获取失败: {data.get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"  ❌ 贡献建议异常: {e}")

if __name__ == "__main__":
    test_opendigger_api()