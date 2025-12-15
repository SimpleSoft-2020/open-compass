from fastapi import APIRouter

router = APIRouter()

# 健康检查
@router.get("/health")
async def api_health():
    return {"status": "ok", "service": "api"}

# 项目信息
@router.get("/project")
async def get_project_info():
    return {
        "name": "开源罗盘",
        "version": "0.1.0",
        "description": "开源贡献者智能导航系统",
        "status": "开发中"
    }