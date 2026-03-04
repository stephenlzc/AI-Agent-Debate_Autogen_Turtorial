#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能体模块
处理智能体的创建和交互
"""

from typing import Dict, Any, Optional, Callable
from autogen import ConversableAgent, GroupChat, GroupChatManager
from openai import OpenAI

from api.config import LLM_CONFIG, CUSTOM_LLM_MODEL

# 创建辩论所需的智能体
def create_agents(topic, supporter_system, supporter_desc, opponent_system, opponent_desc, message_callback=None, token_callback=None):
    """
    创建辩论所需的智能体
    
    Args:
        topic: 辩论主题
        supporter_system: 支持方的system message
        supporter_desc: 支持方的描述
        opponent_system: 反对方的system message
        opponent_desc: 反对方的描述
        message_callback: 消息回调函数，用于实时获取智能体的输出
        token_callback: Token回调函数，用于逐个token流式输出
        
    Returns:
        支持方智能体、反对方智能体和智能体配置
    """
    # 保存配置
    agent_configs = {
        "supporter": {
            "system_message": supporter_system,
            "description": supporter_desc
        },
        "opponent": {
            "system_message": opponent_system,
            "description": opponent_desc
        }
    }

    # 自定义LLM配置
    config_list = LLM_CONFIG

    # 创建支持方智能体
    supporter_agent = ConversableAgent(
        name="supporter",
        system_message=f"""你是支持方辩手。{supporter_system}
        请注意：
        1. 每次发言要有实质性内容，不能返回空消息
        2. 要针对具体论点进行辩论
        3. 使用数据和案例支持你的观点""",
        llm_config={
            "config_list": config_list
        },
        human_input_mode="NEVER",
    )

    # 创建反对方智能体
    opponent_agent = ConversableAgent(
        name="opponent",
        system_message=f"""你是反对方辩手。{opponent_system}
        请注意：
        1. 每次发言要有实质性内容，不能返回空消息
        2. 要针对具体论点进行辩论
        3. 使用数据和案例支持你的观点""",
        llm_config={
            "config_list": config_list
        },
        human_input_mode="NEVER",
    )

    # 设置智能体描述
    supporter_agent.description = supporter_desc
    opponent_agent.description = opponent_desc
    
    # 如果提供了消息回调函数，则设置回调
    if message_callback:
        supporter_agent.register_reply(
            [None, GroupChatManager, GroupChat],
            lambda sender, message: message_callback("supporter", message["content"])
        )
        opponent_agent.register_reply(
            [None, GroupChatManager, GroupChat],
            lambda sender, message: message_callback("opponent", message["content"])
        )
        
    # 如果提供了token回调函数，则我们使用一个特殊的回调来模拟流式输出
    if token_callback:
        # 为了兼容性，我们使用消息回调来模拟流式输出
        # 在消息回调中，我们将完整消息分割为单个字符，并逐个发送
        async def supporter_stream_callback(sender, message):
            content = message.get("content", "")
            # 逐个字符发送
            for char in content:
                await token_callback("supporter", char)
            # 发送结束标记
            await token_callback("supporter", {"finish_reason": "stop", "text": ""})
            # 调用原始消息回调
            if message_callback:
                await message_callback("supporter", content)
        
        async def opponent_stream_callback(sender, message):
            content = message.get("content", "")
            # 逐个字符发送
            for char in content:
                await token_callback("opponent", char)
            # 发送结束标记
            await token_callback("opponent", {"finish_reason": "stop", "text": ""})
            # 调用原始消息回调
            if message_callback:
                await message_callback("opponent", content)
        
        # 注册模拟流式输出的回调
        supporter_agent.register_reply(
            [None, GroupChatManager, GroupChat],
            supporter_stream_callback
        )
        opponent_agent.register_reply(
            [None, GroupChatManager, GroupChat],
            opponent_stream_callback
        )
    
    return supporter_agent, opponent_agent, agent_configs

# 创建裁判智能体
def create_judge_agent(message_callback=None, token_callback=None):
    """
    创建使用自定义LLM的裁判智能体
    
    Args:
        message_callback: 消息回调函数，用于实时获取智能体的输出
        token_callback: Token回调函数，用于逐个token流式输出
        
    Returns:
        裁判智能体
    """
    judge_config = LLM_CONFIG

    judge_agent = ConversableAgent(
        name="judge_Agent",
        system_message="""你是一个中文辩论赛的裁判。你的任务是：
        1. 用中文引导辩论双方进行讨论
        2. 确保双方发言都有实质性内容
        3. 如果发现某方发言内容为空或无意义，要提醒他重新发言
        4. 仔细倾听双方的论点
        5. 基于论点的说服力和论证的完整性来评判胜者
        6. 当你认为辩论已经充分展开且可以做出判断时，你必须：
           - 说出“辩论结束！”
           - 用中文详细说明判决理由
           - 宣布获胜方
        注意：辩论必须在你说出“辩论结束！”并宣布获胜方后才能结束。""",
        llm_config={
            "config_list": judge_config
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: "辩论结束！" in msg["content"]
    )
    
    judge_agent.description = "辩论赛裁判，负责主持辩论并最终决定胜者。"
    
    # 如果提供了消息回调函数，则设置回调
    if message_callback:
        judge_agent.register_reply(
            [None, GroupChatManager, GroupChat],
            lambda sender, message: message_callback("judge", message["content"])
        )
    
    # 如果提供了token回调函数，则我们使用一个特殊的回调来模拟流式输出
    if token_callback:
        # 为了兼容性，我们使用消息回调来模拟流式输出
        async def judge_stream_callback(sender, message):
            content = message.get("content", "")
            # 逐个字符发送
            for char in content:
                await token_callback("judge", char)
            # 发送结束标记
            await token_callback("judge", {"finish_reason": "stop", "text": ""})
            # 调用原始消息回调
            if message_callback:
                await message_callback("judge", content)
        
        # 注册模拟流式输出的回调
        judge_agent.register_reply(
            [None, GroupChatManager, GroupChat],
            judge_stream_callback
        )
    
    return judge_agent

# 测试LLM连接
async def test_llm_connection():
    """
    测试LLM连接和响应是否正常
    
    Returns:
        (success, message)
    """
    try:
        # 只测试自定义LLM
        custom_client = OpenAI(
            api_key=LLM_CONFIG[0]["api_key"],
            base_url=LLM_CONFIG[0]["base_url"]
        )
        
        # 为DeepSeek-R1模型添加系统消息
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好，这是一个测试消息。请回复'测试成功'。"}
        ]
        
        response = custom_client.chat.completions.create(
            model=CUSTOM_LLM_MODEL,
            messages=messages,
            temperature=0.6
        )
        
        if response and response.choices and response.choices[0].message.content:
            return True, "LLM连接测试成功！"
    except Exception as e:
        return False, f"LLM连接测试失败: {str(e)}"
    
    return False, "LLM连接测试失败：未知错误"
