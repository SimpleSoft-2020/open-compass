#!/bin/bash

echo "=== 开始安装开源罗盘依赖 ==="

# 更新pip
echo "1. 更新pip..."
python -m pip install --upgrade pip

# 安装基础依赖
echo "2. 安装基础依赖..."
pip install fastapi==0.104.0 uvicorn[standard]==0.24.0 streamlit==1.28.1

# 安装数据处理库
echo "3. 安装数据处理库..."
pip install pandas==2.1.4 numpy==1.26.3 requests==2.31.0

# 安装GitHub库
echo "4. 安装GitHub API库..."
pip install PyGithub==1.59.1

# 安装数据库和工具
echo "5. 安装数据库和工具..."
pip install sqlalchemy==2.0.23 aiosqlite==0.19.0 python-dotenv==1.0.0 pydantic==2.5.0

# 安装可视化库
echo "6. 安装可视化库..."
pip install plotly==5.17.0

echo "=== 依赖安装完成 ==="
echo ""
echo "启动后端: cd backend && python -m uvicorn main:app --reload"
echo "启动前端: cd frontend && streamlit run app.py"
