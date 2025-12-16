# backend/api/projects.py
from fastapi import APIRouter, HTTPException
from backend.services.project_analyzer import project_analyzer
from backend.services.opendigger_service import opendigger_service
from typing import Dict, Optional

router = APIRouter(prefix="/projects")

@router.get("/{owner}/{repo}")
async def get_project_analysis(owner: str, repo: str, platform: str = "github"):
    """
    获取项目综合分析报告
    """
    try:
        analysis_result = project_analyzer.analyze_project(owner, repo, platform)
        if not analysis_result:
            raise HTTPException(status_code=404, detail="Project data not found")
        
        return {
            "success": True,
            "data": analysis_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/{owner}/{repo}/metrics")
async def get_project_metrics(owner: str, repo: str, platform: str = "github"):
    """
    获取项目核心指标
    """
    try:
        # 获取完整分析结果
        full_analysis = project_analyzer.analyze_project(owner, repo, platform)
        if not full_analysis:
            raise HTTPException(status_code=404, detail="Project data not found")
        
        # 提取关键指标
        key_metrics = {
            "basic_info": full_analysis.get("basic_info", {}),
            "activity_score": full_analysis.get("activity", {}).get("score", 0),
            "community_health": full_analysis.get("community", {}),
            "issues_stats": full_analysis.get("issues", {}),
            "code_quality": full_analysis.get("code_quality", {}),
            "newbie_friendly_score": full_analysis.get("newbie_friendly_score", 0)
        }
        
        return {
            "success": True,
            "data": key_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch metrics: {str(e)}")

@router.get("/{owner}/{repo}/raw/{metric}")
async def get_raw_metric(owner: str, repo: str, metric: str, platform: str = "github"):
    """
    获取原始指标数据
    """
    try:
        # 验证指标名称
        valid_metrics = [
            "activity", "activity_details", "bus_factor", "change_request_age",
            "change_request_resolution_duration", "change_request_response_time",
            "change_requests", "change_requests_accepted", "change_requests_reviews",
            "code_change_lines_add", "code_change_lines_remove", "code_change_lines_sum",
            "contributors", "contributors_detail", "inactive_contributors",
            "issue_age", "issue_resolution_duration", "issue_response_time",
            "issues_closed", "issues_new", "new_contributors", 
            "new_contributors_detail", "technical_fork", "active_dates_and_times"
        ]
        
        if metric not in valid_metrics:
            raise HTTPException(status_code=400, detail=f"Invalid metric name. Valid metrics: {', '.join(valid_metrics)}")
        
        raw_data = opendigger_service.get_specific_metric(owner, repo, metric, platform)
        if raw_data is None:
            raise HTTPException(status_code=404, detail=f"Metric '{metric}' not found")
        
        return {
            "success": True,
            "data": raw_data,
            "metric": metric
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch raw metric: {str(e)}")

@router.get("/{owner}/{repo}/recommendations")
async def get_project_recommendations(owner: str, repo: str, platform: str = "github"):
    """
    获取项目贡献建议
    """
    try:
        # 获取分析结果
        analysis = project_analyzer.analyze_project(owner, repo, platform)
        if not analysis:
            raise HTTPException(status_code=404, detail="Project data not found")
        
        recommendations = []
        
        # 基于新手友好度给出建议
        newbie_score = analysis.get("newbie_friendly_score", 0)
        if newbie_score >= 80:
            recommendations.append({
                "type": "beginner",
                "priority": "high",
                "title": "非常适合新手贡献",
                "description": "该项目对新手非常友好，社区活跃，问题响应迅速"
            })
        elif newbie_score >= 60:
            recommendations.append({
                "type": "beginner",
                "priority": "medium",
                "title": "适合有一定经验的贡献者",
                "description": "项目对新手较友好，建议先熟悉代码库和贡献流程"
            })
        else:
            recommendations.append({
                "type": "beginner",
                "priority": "low",
                "title": "适合经验丰富的贡献者",
                "description": "项目复杂度较高，建议深入了解后再贡献"
            })
        
        # 基于社区健康度给出建议
        community = analysis.get("community", {})
        if community.get("bus_factor", 0) < 3:
            recommendations.append({
                "type": "community",
                "priority": "high",
                "title": "核心贡献者较少",
                "description": "项目依赖少数核心贡献者，你的贡献将非常有价值"
            })
        
        # 基于问题数据给出建议
        issues = analysis.get("issues", {})
        if issues.get("resolution_efficiency", 0) < 50:
            recommendations.append({
                "type": "maintenance",
                "priority": "medium",
                "title": "问题积压较多",
                "description": "项目存在较多未解决问题，修复bug是很好的贡献方向"
            })
        
        # 通用建议
        recommendations.append({
            "type": "general",
            "priority": "medium",
            "title": "阅读贡献指南",
            "description": "建议先仔细阅读项目的CONTRIBUTING.md文件和代码规范"
        })
        
        return {
            "success": True,
            "data": {
                "project": f"{owner}/{repo}",
                "newbie_friendly_score": newbie_score,
                "recommendations": recommendations
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")