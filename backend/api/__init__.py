# backend/api/__init__.py

from fastapi import APIRouter

# 创建主路由器
router = APIRouter()

# 在这里导入并包含子路由
# from . import projects, users, analysis  # 示例：未来可以添加更多模块

# 健康检查端点（必需，因为 main.py 里用它做了根路由）
@router.get("/health")
async def api_health():
    return {"status": "ok", "service": "api"}

# 项目信息端点（可选，但根据您早期的 main.py 设计，它是存在的）
@router.get("/project")
async def get_project_info():
    return {
        "name": "开源罗盘",
        "version": "0.1.0",
        "description": "开源贡献者智能导航系统",
        "status": "开发中"
    }

# 注意：未来可以将不同功能的路由拆分到不同文件（如 projects.py, users.py），
# 然后在这里用 router.include_router() 进行挂载。
