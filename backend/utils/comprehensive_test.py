# backend/utils/comprehensive_test.py
import requests
import json
import time

def test_comprehensive_api():
    """全面测试OpenDigger API功能"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🔍 全面测试OpenDigger API...")
    print("=" * 50)
    
    # 1. 测试基础健康检查
    print("1. 测试基础端点...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   ✅ /health: {response.status_code}")
        if response.status_code == 200:
            print(f"      响应: {response.json()}")
    except Exception as e:
        print(f"   ❌ /health: {e}")
    
    # 2. 测试项目相关API
    test_projects = [
        ("apache", "iotdb"),
        ("X-lab2017", "open-digger"),
        ("easy-graph", "Easy-Graph")
    ]
    
    for i, (owner, repo) in enumerate(test_projects, 2):
        print(f"\n{i}. 测试项目 {owner}/{repo}...")
        
        # 测试综合分析
        try:
            response = requests.get(f"{base_url}/projects/{owner}/{repo}", timeout=15)
            print(f"   综合分析: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"     ✅ 成功获取分析报告")
                    print(f"     🐍 新手友好度: {data['data'].get('newbie_friendly_score', 0)}")
                    print(f"     📈 活跃度分数: {data['data'].get('activity', {}).get('score', 0)}")
                    print(f"     👥 贡献者数量: {data['data'].get('community', {}).get('total_contributors', 0)}")
                else:
                    print(f"     ⚠️  API返回失败: {data.get('detail', 'Unknown error')}")
            else:
                print(f"     ⚠️  HTTP状态码: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 综合分析异常: {e}")
        
        # 测试关键指标
        try:
            response = requests.get(f"{base_url}/projects/{owner}/{repo}/metrics", timeout=10)
            print(f"   关键指标: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"     ✅ 成功获取关键指标")
                    metrics = data.get("data", {})
                    print(f"     📊 活跃度分数: {metrics.get('activity_score', 0)}")
                    print(f"     👥 贡献者数量: {metrics.get('community_health', {}).get('total_contributors', 0)}")
                    print(f"     🐍 新手友好度: {metrics.get('newbie_friendly_score', 0)}")
                else:
                    print(f"     ⚠️  API返回失败: {data.get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"   ❌ 关键指标异常: {e}")
        
        # 测试贡献建议
        try:
            response = requests.get(f"{base_url}/projects/{owner}/{repo}/recommendations", timeout=10)
            print(f"   贡献建议: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"     ✅ 成功获取贡献建议")
                    recommendations = data.get("data", {}).get("recommendations", [])
                    print(f"     💡 建议数量: {len(recommendations)}")
                    if recommendations:
                        print(f"     🎯 首条建议: {recommendations[0].get('title', '')}")
                else:
                    print(f"     ⚠️  API返回失败: {data.get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"   ❌ 贡献建议异常: {e}")
        
        # 测试原始指标数据 (测试几个关键指标)
        key_metrics = ["activity", "contributors", "issues_new", "bus_factor"]
        for metric in key_metrics:
            try:
                response = requests.get(f"{base_url}/projects/{owner}/{repo}/raw/{metric}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        print(f"     ✅ {metric}: 成功获取")
                    else:
                        print(f"     ⚠️  {metric}: {data.get('detail', 'Unknown error')}")
                else:
                    print(f"     ⚠️  {metric}: HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ {metric} 异常: {e}")

    # 3. 测试错误处理
    print(f"\n{len(test_projects) + 2}. 测试错误处理...")
    
    # 测试不存在的项目
    try:
        response = requests.get(f"{base_url}/projects/nonexistent/repo", timeout=10)
        print(f"   不存在项目: {response.status_code}")
        if response.status_code == 404:
            print(f"     ✅ 正确返回404错误")
        else:
            print(f"     ⚠️  应该返回404，实际返回: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
    
    # 测试无效的指标名称
    try:
        response = requests.get(f"{base_url}/projects/apache/iotdb/raw/invalid_metric", timeout=10)
        print(f"   无效指标: {response.status_code}")
        if response.status_code == 404 or response.status_code == 400:
            print(f"     ✅ 正确处理无效指标")
        else:
            print(f"     ⚠️  应该返回400/404，实际返回: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")

    print("\n" + "=" * 50)
    print("🎉 API全面测试完成!")

if __name__ == "__main__":
    test_comprehensive_api()