# backend/api/__init__.py

from fastapi import APIRouter

# 创建主路由器
router = APIRouter()

# 导入并包含子路由
from . import init  # 健康检查等基础路由
from . import projects  # 项目分析相关路由

# 注册子路由
router.include_router(init.router)
router.include_router(projects.router)

# 注意：未来可以将不同功能的路由拆分到不同文件（如 users.py, analysis.py等），
# 然后在这里用 router.include_router() 进行挂载。
