@echo off
echo ========================================
echo CampusBook 二手书交易平台 - 启动脚本
echo ========================================
echo.

echo [1/3] 检查并安装依赖...
pip install Flask Flask-SQLAlchemy Flask-Login

echo.
echo [2/3] 启动应用...
echo 应用将在 http://127.0.0.1:5000 运行
echo 按 Ctrl+C 停止服务
echo.

python app.py
