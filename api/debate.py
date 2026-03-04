#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
辩论模块
处理辩论的启动和管理
"""

import json
from datetime import datetime
import os
from typing import Dict, Any, Optional, Callable
import asyncio

from autogen import GroupChat, GroupChatManager

from api.config import LLM_CONFIG, CUSTOM_LLM_MODEL
from api.agents import create_agents, create_judge_agent

# 保存辩论信息
def save_debate_info(topic, agent_configs, chat_result, max_rounds, model_configs):
    """
    保存辩论相关的所有信息到文件
    
    Args:
        topic: 辩论主题
        agent_configs: 智能体配置
        chat_result: 聊天结果
        max_rounds: 最大辩论轮数
        model_configs: 模型配置
        
    Returns:
        保存的文件路径
    """
    # 创建保存目录
    save_dir = "debates"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 提取聊天历史并转换为可序列化格式
    chat_history = []
    for msg in chat_result.chat_history:
        if isinstance(msg, dict):
            # 复制消息字典，确保所有值都是可序列化的
            serializable_msg = {
                "name": msg.get("name", "Unknown"),
                "content": msg.get("content", ""),
                "role": msg.get("role", "unknown")
            }
            chat_history.append(serializable_msg)
    
    # 构建完整的辩论信息
    debate_info = {
        "topic": topic,
        "timestamp": timestamp,
        "max_rounds": max_rounds,
        "agent_configs": agent_configs,
        "model_configs": model_configs,
        "chat_history": chat_history
    }
    
    # 保存为JSON文件
    json_file = os.path.join(save_dir, f"debate_{timestamp}.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(debate_info, f, ensure_ascii=False, indent=2)
    
    # 保存为纯文本文件，便于阅读
    chat_file = os.path.join(save_dir, f"debate_{timestamp}_chat.txt")
    with open(chat_file, 'w', encoding='utf-8') as f:
        f.write(f"辩论主题: {topic}\n")
        f.write(f"时间: {timestamp}\n")
        f.write("="*50 + "\n\n")
        
        # 写入对话内容
        for msg in chat_history:
            speaker = msg["name"]
            content = msg["content"]
            f.write(f"{speaker}:\n{content}\n\n")
    
    return {
        "json_file": json_file,
        "chat_file": chat_file
    }

# 启动辩论
async def start_debate(config, message_callback=None, token_callback=None):
    """
    启动辩论
    
    Args:
        config: 辩论配置
        message_callback: 消息回调函数，用于实时获取智能体的输出
        token_callback: Token回调函数，用于逐个token流式输出
        
    Returns:
        辩论结果
    """
    topic = config.topic
    max_rounds = config.max_rounds
    
    # 保存模型配置
    model_configs = {
        "model_name": CUSTOM_LLM_MODEL,
        "base_url": LLM_CONFIG[0]["base_url"],
        "api_key": "****"  # 不保存实际的API key
    }
    
    # 创建智能体
    supporter_agent, opponent_agent, agent_configs = create_agents(
        topic, 
        config.supporter_system, 
        config.supporter_desc, 
        config.opponent_system, 
        config.opponent_desc,
        message_callback,
        token_callback
    )
    judge_agent = create_judge_agent(message_callback, token_callback)
    
    # 创建群组聊天
    group_chat = GroupChat(
        agents=[supporter_agent, opponent_agent, judge_agent],
        messages=[],
        send_introductions=True,
        speaker_selection_method="auto",
        max_round=max_rounds
    )

    # 创建群组聊天管理器
    group_chat_manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={
            "config_list": LLM_CONFIG
        },
    )
    
    # 启动辩论
    chat_result = await judge_agent.a_initiate_chat(
        group_chat_manager,
        message=f"""这场关于'{topic}'的辩论现在开始。
        1. 请双方辩手认真倾听对方观点
        2. 每次发言必须有实质性内容
        3. 使用具体的数据和案例支持论点
        4. 遵守裁判的指示
        
        现在请支持方先发言。""",
        summary_method="reflection_with_llm",
    )
    
    # 保存辩论信息
    files = save_debate_info(topic, agent_configs, chat_result, max_rounds, model_configs)
    
    # 返回结果
    return {
        "topic": topic,
        "max_rounds": max_rounds,
        "chat_history": [
            {
                "name": msg.get("name", "Unknown"),
                "content": msg.get("content", ""),
                "role": msg.get("role", "unknown")
            }
            for msg in chat_result.chat_history if isinstance(msg, dict)
        ],
        "files": files
    }
