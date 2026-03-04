#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据模型模块
定义API使用的数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class DebateConfig(BaseModel):
    """辩论配置模型"""
    topic: str
    max_rounds: int
    supporter_system: str
    supporter_desc: str
    opponent_system: str
    opponent_desc: str
    enable_speech: bool = True  # 是否启用语音

class AgentMessage(BaseModel):
    """智能体消息模型"""
    name: str
    content: str
    role: str = "unknown"

class SpeechChunk(BaseModel):
    """语音分块模型"""
    file_path: str
    file_id: str
    audio_base64: str

class SpeechResult(BaseModel):
    """语音生成结果模型"""
    chunks: List[SpeechChunk]
    file_id: str
    total_chunks: int

class DebateResult(BaseModel):
    """辩论结果模型"""
    topic: str
    max_rounds: int
    chat_history: List[AgentMessage]
    files: Dict[str, str]

class WebSocketTextMessage(BaseModel):
    """文本消息模型"""
    type: str = "text"
    agent: str
    content: str

class WebSocketSpeechMessage(BaseModel):
    """语音消息模型"""
    type: str = "speech"
    agent: str
    content: str
    speech: SpeechChunk

class WebSocketTokenMessage(BaseModel):
    """Token流消息模型"""
    type: str = "token"
    agent: str
    token: str
    is_end: bool = False

class WebSocketMessage(BaseModel):
    """消息模型"""
    type: str
    agent: str
    content: Optional[str] = None
    speech: Optional[SpeechChunk] = None
    token: Optional[str] = None
    is_end: Optional[bool] = None

class WebSocketResponse(BaseModel):
    """响应模型"""
    status: str
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
