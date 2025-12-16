# backend/docs/api_usage_guide.py (创建这个文件作为文档)
"""
OpenDigger API 使用指南
=====================

## 基础端点

### 健康检查
GET /api/v1/health
检查API服务状态

### 项目综合分析
GET /api/v1/projects/{owner}/{repo}
获取项目的完整分析报告

### 项目关键指标
GET /api/v1/projects/{owner}/{repo}/metrics
获取项目的核心指标数据

### 项目贡献建议
GET /api/v1/projects/{owner}/{repo}/recommendations
获取针对项目的贡献建议

### 原始指标数据
GET /api/v1/projects/{owner}/{repo}/raw/{metric}
获取特定指标的原始数据

## 支持的指标

- activity: 活跃度
- contributors: 贡献者
- issues_new: 新问题
- issues_closed: 已关闭问题
- bus_factor: Bus Factor
- change_requests: 变更请求
- change_requests_accepted: 已接受的变更请求
- code_change_lines_sum: 代码变更行数总和

## 使用示例

### Python requests 示例
```python
import requests

# 获取项目分析报告
response = requests.get("http://localhost:8000/api/v1/projects/apache/iotdb")
if response.status_code == 200:
    data = response.json()
    print(data)

# 获取原始指标数据
response = requests.get("http://localhost:8000/api/v1/projects/apache/iotdb/raw/activity")
if response.status_code == 200:
    activity_data = response.json()
    print(activity_data)