#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
服务器入口
启动FastAPI服务器
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.debate_view import debate_view_router
from api.config import SERVER_HOST, SERVER_PORT

# 创建FastAPI应用
app = FastAPI(
    title="辩论系统API", 
    description="提供辩论系统的API接口，用于构建辩论应用程序",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)
app.include_router(debate_view_router)  # 路由器已经定义了前缀，不需要再添加

if __name__ == "__main__":
    # 强制使用端口8001
    port = 8001
    print(f"启动服务器：http://{SERVER_HOST}:{port}")
    uvicorn.run(app, host=SERVER_HOST, port=port)
