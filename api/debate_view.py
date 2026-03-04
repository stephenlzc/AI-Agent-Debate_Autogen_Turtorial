#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
辩论视图API模块
提供辩论视图页面所需的API接口
"""

from fastapi import APIRouter, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import random

# 创建路由
debate_view_router = APIRouter(prefix="/debate_view", tags=["debate_view"])

# 定义模型
class MessageItem(BaseModel):
    """消息项模型"""
    type: str  # 消息类型: "host", "blue", "red"
    content: str  # 消息内容
    displayContent: str = ""  # 用于打字机效果的显示内容
    isTyping: bool = False  # 是否正在打字
    typingIndex: int = 0  # 打字索引

class DebateInfo(BaseModel):
    """辩论信息模型"""
    topic: Dict[str, Any]  # 辩论主题
    selectedTeam: str  # 选择的队伍
    blueStance: str  # 蓝队立场
    redStance: str  # 红队立场
    bluePlayerType: str  # 蓝队选手类型
    redPlayerType: str  # 红队选手类型
    useVoice: bool  # 是否使用语音

class DebateViewData(BaseModel):
    """辩论视图数据模型"""
    debateInfo: DebateInfo  # 辩论信息
    debateRounds: int  # 辩论轮数
    currentRound: int  # 当前轮数
    messages: List[MessageItem]  # 消息列表

# 示例数据
def get_sample_debate_data() -> Dict[str, Any]:
    """获取示例辩论数据"""
    return {
        "debateInfo": {
            "topic": {"id": 0, "title": "结婚还是做单身狗", "description": ""},
            "selectedTeam": "blue",
            "blueStance": "结婚",
            "redStance": "单身狗",
            "bluePlayerType": "保守型",
            "redPlayerType": "激进型",
            "useVoice": True
        },
        "debateRounds": 15,
        "messages": [
            {
                "type": "host",
                "content": "各位观众朋友们大家好，欢迎来到本次辩论。今天的辩题是《结婚还是做单身狗》。蓝队将支持「结婚」，红队将支持「单身狗」。辩论共计15轮，现在开始第一轮辩论。",
                "displayContent": "",
                "isTyping": False,
                "typingIndex": 0
            },
            {
                "type": "blue",
                "content": "家庭温暖和经济稳定性: 结婚后可以享受家庭的温暖，有人陪伴和照顾，尤其是在遇到困难时有人分担。",
                "displayContent": "",
                "isTyping": False,
                "typingIndex": 0
            },
            {
                "type": "red",
                "content": "自由和独立: 单身生活最大的优点是自由，可以自由安排自己的时间和生活，无需考虑他人的感受和需求。经济上也更自由，可以随心所欲地花钱而不用担心另一半的意见",
                "displayContent": "",
                "isTyping": False,
                "typingIndex": 0
            },
            {
                "type": "host",
                "content": "第一轮辩论结束，双方观点鲜明。现在进入第二轮辩论，请双方针对对方观点进行深入辩论。",
                "displayContent": "",
                "isTyping": False,
                "typingIndex": 0
            },
            {
                "type": "blue",
                "content": "对于红队提到的自由问题，我认为婚姻并不会完全剪除个人自由。婚姻是两个人共同成长的过程，可以通过沟通和相互尊重来保持各自的空间和自由。",
                "displayContent": "",
                "isTyping": False,
                "typingIndex": 0
            },
            {
                "type": "red",
                "content": "蓝队提到的家庭温暖确实存在，但这种温暖也可以从朋友和家人关系中获得。而且，婚姻生活中的矛盾和压力可能会让这种温暖变成负担，单身生活可以避免这些问题。",
                "displayContent": "",
                "isTyping": False,
                "typingIndex": 0
            }
        ]
    }

# 定义路由
@debate_view_router.get("/data")
async def get_debate_view_data():
    """
    获取辩论视图数据 (Mock接口)
    
    Returns:
        模拟的辩论视图数据
    """
    return get_sample_debate_data()

# 注意：根据需求，已移除/generate接口

@debate_view_router.post("/save")
async def save_debate_info(data: Dict[str, Any] = Body(...)):
    """
    保存辩论信息 (Mock接口)
    
    Args:
        data: 辩论信息
        
    Returns:
        模拟的保存结果
    """
    # 实际应用中，这里应该将数据保存到数据库
    return {"success": True, "message": "辩论信息保存成功"}
