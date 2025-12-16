# backend/utils/verify_api_functionality.py
import requests
import json

def verify_api_functionality():
    """验证API各功能模块是否正常工作"""
    base_url = "http://localhost:8000/api/v1"
    
    print("🔍 验证API功能模块...")
    print("=" * 50)
    
    # 测试项目: apache/iotdb
    owner, repo = "apache", "iotdb"
    print(f"测试项目: {owner}/{repo}")
    
    # 1. 验证数据分析功能
    print("\n1. 验证数据分析功能...")
    try:
        response = requests.get(f"{base_url}/projects/{owner}/{repo}", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                analysis = data.get("data", {})
                print("   ✅ 数据分析功能正常")
                print(f"      项目名称: {analysis.get('basic_info', {}).get('full_name')}")
                print(f"      活跃度分数: {analysis.get('activity', {}).get('score', 0)}")
                print(f"      社区健康度: {analysis.get('community', {}).get('total_contributors', 0)} 贡献者")
                print(f"      新手友好度: {analysis.get('newbie_friendly_score', 0)}")
            else:
                print("   ❌ 数据分析返回失败")
        else:
            print(f"   ❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 2. 验证指标提取功能
    print("\n2. 验证指标提取功能...")
    try:
        response = requests.get(f"{base_url}/projects/{owner}/{repo}/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                metrics = data.get("data", {})
                print("   ✅ 指标提取功能正常")
                required_fields = ["basic_info", "activity_score", "community_health", 
                                 "issues_stats", "newbie_friendly_score"]
                for field in required_fields:
                    if field in metrics:
                        print(f"      ✅ {field}: 已提供")
                    else:
                        print(f"      ❌ {field}: 缺失")
            else:
                print("   ❌ 指标提取返回失败")
        else:
            print(f"   ❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 3. 验证建议生成功能
    print("\n3. 验证建议生成功能...")
    try:
        response = requests.get(f"{base_url}/projects/{owner}/{repo}/recommendations", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                recommendations_data = data.get("data", {})
                recommendations = recommendations_data.get("recommendations", [])
                print("   ✅ 建议生成功能正常")
                print(f"      生成建议数量: {len(recommendations)}")
                for i, rec in enumerate(recommendations[:3]):  # 显示前3个建议
                    print(f"      建议{i+1}: {rec.get('title', '')}")
            else:
                print("   ❌ 建议生成返回失败")
        else:
            print(f"   ❌ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 4. 验证原始数据访问功能
    print("\n4. 验证原始数据访问功能...")
    test_metrics = ["activity", "contributors", "issues_new", "bus_factor"]
    for metric in test_metrics:
        try:
            response = requests.get(f"{base_url}/projects/{owner}/{repo}/raw/{metric}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"   ✅ {metric}: 可访问")
                    raw_data = data.get("data", {})
                    if isinstance(raw_data, dict):
                        print(f"      数据结构: {type(raw_data).__name__}, 键数量: {len(raw_data)}")
                    else:
                        print(f"      数据类型: {type(raw_data).__name__}")
                else:
                    print(f"   ⚠️  {metric}: API返回失败 - {data.get('detail', 'Unknown')}")
            elif response.status_code == 404:
                print(f"   ⚠️  {metric}: 数据不存在")
            else:
                print(f"   ⚠️  {metric}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {metric} 异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API功能验证完成!")

if __name__ == "__main__":
    verify_api_functionality()