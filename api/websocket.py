#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WebSocket连接管理模块
管理WebSocket连接和消息发送
"""

import json
import logging
from typing import List, Dict, Any, Union
from fastapi import WebSocket
from pydantic import BaseModel

# 配置日志
logger = logging.getLogger(__name__)

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
        
        # 复制列表避免修改迭代中的列表（防止其他协程修改连接列表）
        connections = self.active_connections.copy()
        
        # 广播消息到每个连接，单独处理异常
        disconnected = []
        for connection in connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                # 记录错误但继续处理其他连接
                logger.warning(f"广播消息失败，准备断开连接: {str(e)}")
                disconnected.append(connection)
        
        # 断开失败的连接
        for connection in disconnected:
            try:
                self.disconnect(connection)
                # 尝试关闭连接
                await connection.close()
            except Exception as e:
                logger.debug(f"关闭连接时出错: {str(e)}")

# 创建全局连接管理器实例
manager = ConnectionManager()
