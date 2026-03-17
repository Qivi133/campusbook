# Vercel Serverless Flask 应用入口
from app import app

# Vercel Serverless 需要导出 app
handler = app
