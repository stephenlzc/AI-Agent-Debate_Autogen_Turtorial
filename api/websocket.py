#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WebSocket连接管理模块
管理WebSocket连接和消息发送
"""

import json
from typing import List, Dict, Any, Union
from fastapi import WebSocket
from pydantic import BaseModel

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        连接WebSocket
        
        Args:
            websocket: WebSocket连接
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        断开WebSocket连接
        
        Args:
            websocket: WebSocket连接
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: Union[str, Dict, BaseModel], websocket: WebSocket):
        """
        发送消息到指定WebSocket
        
        Args:
            message: 消息内容，可以是字符串、字典或Pydantic模型
            websocket: WebSocket连接
        """
        if isinstance(message, str):
            # 如果是字符串，直接发送
            await websocket.send_text(message)
        elif isinstance(message, BaseModel):
            # 如果是Pydantic模型，转换为JSON字符串
            await websocket.send_text(message.json())
        elif isinstance(message, dict):
            # 如果是字典，转换为JSON字符串
            await websocket.send_text(json.dumps(message))
        else:
            # 其他类型，尝试转换为字符串
            await websocket.send_text(str(message))

    async def send_json(self, data: Dict[str, Any], websocket: WebSocket):
        """
        发送JSON数据到指定WebSocket
        
        Args:
            data: JSON数据
            websocket: WebSocket连接
        """
        await websocket.send_json(data)

    async def broadcast(self, message: Union[str, Dict, BaseModel]):
        """
        广播消息到所有WebSocket
        
        Args:
            message: 消息内容，可以是字符串、字典或Pydantic模型
        """
        # 将消息转换为字符串
        if isinstance(message, BaseModel):
            message_str = message.json()
        elif isinstance(message, dict):
            message_str = json.dumps(message)
        else:
            message_str = str(message)
            
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message_str)

# 创建全局连接管理器实例
manager = ConnectionManager()
