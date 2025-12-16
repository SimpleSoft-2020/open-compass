# backend/services/project_analyzer.py
from backend.services.opendigger_service import opendigger_service
from typing import Dict, Any, List
import json

class ProjectAnalyzer:
    def __init__(self):
        self.opendigger = opendigger_service
    
    def analyze_project(self, owner: str, repo: str, platform: str = "github") -> Dict[str, Any]:
        """
        使用OpenDigger数据综合分析项目各项指标
        """
        # 获取关键指标数据
        metrics = self.opendigger.get_all_metrics(owner, repo, platform)
        
        # 整合数据
        project_metrics = {
            "basic_info": {
                "full_name": f"{owner}/{repo}",
                "owner": owner,
                "name": repo,
                "platform": platform
            },
            "activity": self._analyze_activity(metrics),
            "community": self._analyze_community(metrics),
            "issues": self._analyze_issues(metrics),
            "code_quality": self._analyze_code_quality(metrics),
            "newbie_friendly_score": self._calculate_newbie_friendly_score(metrics)
        }
        
        return project_metrics
    
    def _analyze_activity(self, metrics: Dict) -> Dict:
        """分析活跃度数据"""
        activity_data = metrics.get("activity", {})
        if not activity_data:
            return {"score": 0, "trend": "unknown", "recent_months": []}
        
        try:
            # 获取最近12个月的数据
            sorted_months = sorted(activity_data.keys(), reverse=True)[:12]
            recent_data = [{"month": month, "value": activity_data[month]} for month in sorted_months]
            
            # 计算平均活跃度
            recent_values = [item["value"] for item in recent_data]
            avg_score = sum(recent_values) / len(recent_values) if recent_values else 0
            
            # 判断趋势（最近3个月）
            trend = "stable"
            if len(recent_values) >= 3:
                recent_3 = recent_values[:3]
                older_3 = recent_values[3:6] if len(recent_values) >= 6 else []
                if older_3:
                    recent_avg = sum(recent_3) / len(recent_3)
                    older_avg = sum(older_3) / len(older_3)
                    if recent_avg > older_avg * 1.1:  # 增长超过10%
                        trend = "increasing"
                    elif recent_avg < older_avg * 0.9:  # 下降超过10%
                        trend = "decreasing"
            
            return {
                "score": round(avg_score, 2),
                "trend": trend,
                "recent_months": recent_data[:6]  # 返回最近6个月数据
            }
        except Exception as e:
            print(f"Error analyzing activity: {e}")
            return {"score": 0, "trend": "unknown", "recent_months": []}
    
    def _analyze_community(self, metrics: Dict) -> Dict:
        """分析社区数据"""
        contributors_data = metrics.get("contributors", {})
        bus_factor_data = metrics.get("bus_factor", {})
        
        result = {
            "total_contributors": 0,
            "active_contributors": 0,
            "bus_factor": 0,
            "key_contributors": []
        }
        
        try:
            # 分析贡献者数据
            if contributors_data and isinstance(contributors_data, dict):
                result["total_contributors"] = len(contributors_data)
                
                # 计算活跃贡献者（贡献次数大于平均值的贡献者）
                contributions = list(contributors_data.values())
                if contributions:
                    avg_contributions = sum(contributions) / len(contributions)
                    active_contributors = [name for name, count in contributors_data.items() 
                                         if count > avg_contributions]
                    result["active_contributors"] = len(active_contributors)
                    
                    # 获取关键贡献者（前5名）
                    sorted_contributors = sorted(contributors_data.items(), 
                                              key=lambda x: x[1], reverse=True)[:5]
                    result["key_contributors"] = [
                        {"name": name, "contributions": count} 
                        for name, count in sorted_contributors
                    ]
            
            # 分析Bus Factor
            if bus_factor_data:
                if isinstance(bus_factor_data, dict):
                    result["bus_factor"] = bus_factor_data.get("bus_factor", 
                                                            bus_factor_data.get("value", 0))
                elif isinstance(bus_factor_data, (int, float)):
                    result["bus_factor"] = bus_factor_data
            
        except Exception as e:
            print(f"Error analyzing community: {e}")
        
        return result
    
    def _analyze_issues(self, metrics: Dict) -> Dict:
        """分析问题数据"""
        issues_new_data = metrics.get("issues_new", {})
        issues_closed_data = metrics.get("issues_closed", {})
        issue_response_data = metrics.get("issue_response_time", {})
        
        result = {
            "new_issues": 0,
            "closed_issues": 0,
            "resolution_efficiency": 0,
            "avg_response_time": 0
        }
        
        try:
            # 获取最近一个月的数据
            if issues_new_data:
                latest_month = max(issues_new_data.keys())
                result["new_issues"] = issues_new_data.get(latest_month, 0)
            
            if issues_closed_data:
                latest_month = max(issues_closed_data.keys())
                result["closed_issues"] = issues_closed_data.get(latest_month, 0)
            
            # 计算解决效率
            if result["new_issues"] > 0:
                result["resolution_efficiency"] = round(
                    (result["closed_issues"] / result["new_issues"]) * 100, 2
                )
            
            # 分析响应时间
            if issue_response_data and isinstance(issue_response_data, dict):
                # 计算平均响应时间
                response_times = list(issue_response_data.values())
                if response_times:
                    result["avg_response_time"] = round(sum(response_times) / len(response_times), 2)
                    
        except Exception as e:
            print(f"Error analyzing issues: {e}")
        
        return result
    
    def _analyze_code_quality(self, metrics: Dict) -> Dict:
        """分析代码质量相关数据"""
        change_requests_data = metrics.get("change_requests", {})
        change_requests_accepted_data = metrics.get("change_requests_accepted", {})
        code_changes_sum_data = metrics.get("code_change_lines_sum", {})
        
        result = {
            "pr_acceptance_rate": 0,
            "code_changes": 0,
            "activity_level": "low"
        }
        
        try:
            # 计算PR接受率
            if change_requests_data and change_requests_accepted_data:
                # 获取最近有数据的月份
                common_months = set(change_requests_data.keys()) & set(change_requests_accepted_data.keys())
                if common_months:
                    latest_month = max(common_months)
                    total_prs = change_requests_data.get(latest_month, 0)
                    accepted_prs = change_requests_accepted_data.get(latest_month, 0)
                    
                    if total_prs > 0:
                        result["pr_acceptance_rate"] = round((accepted_prs / total_prs) * 100, 2)
            
            # 获取代码变更量
            if code_changes_sum_data:
                latest_month = max(code_changes_sum_data.keys())
                result["code_changes"] = code_changes_sum_data.get(latest_month, 0)
            
            # 根据代码变更量判断活跃度
            if result["code_changes"] > 10000:
                result["activity_level"] = "high"
            elif result["code_changes"] > 1000:
                result["activity_level"] = "medium"
            else:
                result["activity_level"] = "low"
                
        except Exception as e:
            print(f"Error analyzing code quality: {e}")
        
        return result
    
    def _calculate_newbie_friendly_score(self, metrics: Dict) -> float:
        """
        计算新手友好度分数
        综合考虑项目活跃度、社区健康度、问题处理效率等因素
        """
        score = 0.0
        
        try:
            # 基于活跃度 (25%权重)
            activity = self._analyze_activity(metrics)
            activity_score = activity.get("score", 0)
            score += min(activity_score / 1000, 0.25)  # 1000分以上得满分
            
            # 基于贡献者数量 (20%权重)
            community = self._analyze_community(metrics)
            contributor_count = community.get("total_contributors", 0)
            score += min(contributor_count / 100, 0.20)  # 100个贡献者以上得满分
            
            # 基于Bus Factor (20%权重)
            bus_factor = community.get("bus_factor", 0)
            score += min(bus_factor / 10, 0.20)  # 10以上得满分
            
            # 基于问题解决效率 (20%权重)
            issues = self._analyze_issues(metrics)
            resolution_efficiency = issues.get("resolution_efficiency", 0)
            score += min(resolution_efficiency / 100, 0.20)  # 100%解决率得满分
            
            # 基于PR接受率 (15%权重)
            code_quality = self._analyze_code_quality(metrics)
            pr_acceptance_rate = code_quality.get("pr_acceptance_rate", 0)
            score += min(pr_acceptance_rate / 100, 0.15)  # 100%接受率得满分
            
        except Exception as e:
            print(f"Error calculating newbie friendly score: {e}")
        
        return round(score * 100, 2)

# 创建全局实例
project_analyzer = ProjectAnalyzer()