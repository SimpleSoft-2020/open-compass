# backend/services/opendigger_service.py
import requests
from typing import Dict, Any, Optional
import json
import os

class OpenDiggerService:
    def __init__(self):
        # 根据文档，使用正确的基础URL
        self.base_url = "https://oss.open-digger.cn"
        self.headers = {
            "User-Agent": "OpenCompass/1.0",
            "Accept": "application/json"
        }
        # 用于本地测试的本地文件路径（如果需要）
        self.local_data_path = "opendigger-api"
    
    def get_repo_base_url(self, owner: str, repo: str, platform: str = "github") -> str:
        """构建仓库基础URL"""
        return f"{self.base_url}/{platform}/{owner}/{repo}"
    
    def get_specific_metric(self, owner: str, repo: str, metric: str, platform: str = "github") -> Optional[Dict]:
        """获取特定指标数据"""
        # 首先尝试从网络获取
        base_url = self.get_repo_base_url(owner, repo, platform)
        url = f"{base_url}/{metric}.json"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch {url}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        
        # 如果网络获取失败，尝试从本地文件获取（开发测试用）
        try:
            local_file = os.path.join(self.local_data_path, f"{metric}.json")
            if os.path.exists(local_file):
                with open(local_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading local file {local_file}: {e}")
        
        return None
    
    def get_all_metrics(self, owner: str, repo: str, platform: str = "github") -> Dict[str, Any]:
        """获取所有可用指标数据"""
        metrics = {}
        
        # 所有可用的指标
        metric_names = [
            "activity", "activity_details",
            "bus_factor",
            "change_request_age",
            "change_request_resolution_duration",
            "change_request_response_time",
            "change_requests",
            "change_requests_accepted",
            "change_requests_reviews",
            "code_change_lines_add",
            "code_change_lines_remove",
            "code_change_lines_sum",
            "contributors",
            "contributors_detail",
            "inactive_contributors",
            "issue_age",
            "issue_resolution_duration",
            "issue_response_time",
            "issues_closed",
            "issues_new",
            "new_contributors",
            "new_contributors_detail",
            "technical_fork",
            "active_dates_and_times"
        ]
        
        for metric in metric_names:
            metrics[metric] = self.get_specific_metric(owner, repo, metric, platform)
        
        return metrics

# 创建全局实例
opendigger_service = OpenDiggerService()