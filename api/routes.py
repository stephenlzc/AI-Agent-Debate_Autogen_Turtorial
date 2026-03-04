#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
路由模块
定义API路由
"""

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from typing import Dict, Any

from api.models import DebateConfig, WebSocketMessage, WebSocketTextMessage, WebSocketSpeechMessage
from api.agents import test_llm_connection
from api.debate import start_debate
from api.websocket import manager
from api.speech import speech_service
from api.config import SPEECH_ENABLED

# 创建路由
router = APIRouter()

@router.get("/")
async def root():
    """
    根路由
    
    Returns:
        欢迎信息
    """
    return {"message": "欢迎使用辩论系统API"}

@router.get("/test_connection")
async def test_connection():
    """
    测试LLM连接
    
    Returns:
        连接测试结果
    """
    success, message = await test_llm_connection()
    return {"success": success, "message": message}

@router.post("/debate")
async def debate(config: DebateConfig):
    """
    启动一场辩论（同步API）
    
    Args:
        config: 辩论配置
        
    Returns:
        辩论结果
    """
    result = await start_debate(config)
    return result

@router.post("/text_to_speech")
async def text_to_speech(data: Dict[str, Any] = Body(...)):
    """
    文本转语音API
    
    Args:
        data: 请求数据，包含 text 和 agent_name
        
    Returns:
        语音生成结果
    """
    text = data.get("text", "")
    agent_name = data.get("agent_name", "supporter")
    
    if not text:
        return {"error": "文本不能为空"}
    
    result = await speech_service.text_to_speech(text, agent_name)
    return result

@router.post("/generate_speech_chunks")
async def generate_speech_chunks(data: Dict[str, Any] = Body(...)):
    """
    生成语音分块API
    
    Args:
        data: 请求数据，包含 text、agent_name 和 chunk_size
        
    Returns:
        语音分块生成结果
    """
    text = data.get("text", "")
    agent_name = data.get("agent_name", "supporter")
    chunk_size = data.get("chunk_size", 100)
    
    if not text:
        return {"error": "文本不能为空"}
    
    result = await speech_service.generate_speech_chunks(text, agent_name, chunk_size)
    return result

@router.websocket("/ws/debate")
async def websocket_debate(websocket: WebSocket):
    """
    通过WebSocket启动一场辩论，实时返回辩论内容
    
    Args:
        websocket: WebSocket连接
    """
    await manager.connect(websocket)
    try:
        # 接收辩论配置
        config_data = await websocket.receive_text()
        config = DebateConfig.parse_raw(config_data)
        
        # 定义消息回调函数
        async def message_callback(agent_name, content):
            # 创建文本消息
            text_message = WebSocketTextMessage(
                type="text",
                agent=agent_name,
                content=content
            )
            
            # 发送文本消息
            await manager.send_message(
                text_message.json(),
                websocket
            )
            
            # 如果启用了语音，生成并发送语音
            if SPEECH_ENABLED and config.enable_speech:
                try:
                    # 生成语音
                    speech_result = await speech_service.text_to_speech(content, agent_name)
                    
                    if "error" not in speech_result:
                        # 创建语音消息
                        speech_message = WebSocketSpeechMessage(
                            type="speech",
                            agent=agent_name,
                            content=content,
                            speech=speech_result
                        )
                        
                        # 发送语音消息
                        await manager.send_message(
                            speech_message.json(),
                            websocket
                        )
                except Exception as e:
                    print(f"语音生成失败: {str(e)}")
        
        # 定义Token流回调函数
        async def token_callback(agent_name, token):
            try:
                # 创建 Token 消息
                # 处理不同类型的token参数
                if isinstance(token, dict):
                    is_end = token.get("finish_reason") is not None
                    token_text = token.get("text", "")
                elif isinstance(token, str):
                    is_end = False
                    token_text = token
                else:
                    # 如果是其他类型，尝试转换为字符串
                    is_end = False
                    token_text = str(token)
                
                # 只在有实际内容或结束标记时发送
                if token_text or is_end:
                    token_message = WebSocketTokenMessage(
                        type="token",
                        agent=agent_name,
                        token=token_text,
                        is_end=is_end
                    )
                    
                    # 发送Token消息
                    await manager.send_message(
                        token_message.json(),
                        websocket
                    )
            except Exception as e:
                print(f"Token回调处理错误: {str(e)}")
        
        # 启动辩论
        result = await start_debate(config, message_callback, token_callback)
        
        # 发送辩论结果
        await manager.send_message(json.dumps({"status": "completed", "result": result}), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_message(json.dumps({"status": "error", "message": str(e)}), websocket)
        manager.disconnect(websocket)
