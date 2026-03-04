#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
这是一个基于AutoGen框架的多智能体对话系统
实现了一个自定义主题的辩论场景
包含三个智能体：正方支持者、反方支持者和裁判

作者：[您的名字]
日期：[创建日期]
"""

# 系统库导入
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# 第三方库导入
from autogen import ConversableAgent, GroupChat, GroupChatManager
from openai import OpenAI

# 加载.env文件中的环境变量
load_dotenv()

# API密钥配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CUSTOM_LLM_API_KEY = os.getenv('CUSTOM_LLM_API_KEY')
CUSTOM_LLM_API_BASE = os.getenv('CUSTOM_LLM_API_BASE')
CUSTOM_LLM_MODEL = os.getenv('CUSTOM_LLM_MODEL')

# 检查必要的环境变量
if not all([OPENAI_API_KEY, CUSTOM_LLM_API_KEY, CUSTOM_LLM_API_BASE, CUSTOM_LLM_MODEL]):
    raise ValueError("请确保.env文件中包含所有必要的配置项")

def test_llm_connection():
    """
    测试LLM连接和响应是否正常
    """
    print("正在测试LLM连接...")
    try:
        # 只测试自定义LLM
        custom_client = OpenAI(
            api_key=CUSTOM_LLM_API_KEY,
            base_url=CUSTOM_LLM_API_BASE
        )
        
        response = custom_client.chat.completions.create(
            model=CUSTOM_LLM_MODEL,
            messages=[
                {"role": "user", "content": "你好，这是一个测试消息。请回复'测试成功'。"}
            ]
        )
        
        if response and response.choices and response.choices[0].message.content:
            print("LLM连接测试成功！")
            return True
    except Exception as e:
        print(f"LLM连接测试失败: {str(e)}")
        return False

def test_autogen_config():
    """
    测试AutoGen配置是否正常
    """
    print("正在测试AutoGen配置...")
    try:
        config_list = [{
            "model": CUSTOM_LLM_MODEL,
            "api_key": CUSTOM_LLM_API_KEY,
            "base_url": CUSTOM_LLM_API_BASE
        }]

        # 创建一个测试agent
        test_agent = ConversableAgent(
            name="test_agent",
            system_message="你是一个测试agent。",
            llm_config={"config_list": config_list},
            human_input_mode="NEVER",
        )

        # 创建一个测试群组聊天管理器
        test_manager = GroupChatManager(
            groupchat=GroupChat(
                agents=[test_agent],
                messages=[],
                max_round=1
            ),
            llm_config={"config_list": config_list},
        )

        print("AutoGen配置测试成功！")
        return True
    except Exception as e:
        print(f"AutoGen配置测试失败: {str(e)}")
        return False

def save_debate_info(topic, agent_configs, chat_result, max_rounds, model_configs):
    """
    保存辩论相关的所有信息到文件
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
    
    # 准备保存的数据
    debate_data = {
        "topic": topic,
        "timestamp": timestamp,
        "max_rounds": max_rounds,
        "model_configs": model_configs,
        "agent_configs": agent_configs,
        "chat_history": chat_history  # 使用处理过的聊天历史
    }
    
    # 保存辩论配置和结果
    config_file = os.path.join(save_dir, f"debate_{timestamp}.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(debate_data, f, ensure_ascii=False, indent=2)
    
    # 保存对话记录
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
    
    print(f"\n辩论信息已保存到目录: {save_dir}")
    print(f"配置文件: debate_{timestamp}.json")
    print(f"对话记录: debate_{timestamp}_chat.txt")

def create_agents(topic):
    """
    创建辩论所需的智能体
    """
    print("\n=== 请输入Agent配置 ===")
    print("\n支持方配置:")
    supporter_system = input("请输入支持方的system message: ")
    supporter_desc = input("请输入支持方的描述: ")
    
    print("\n反对方配置:")
    opponent_system = input("请输入反对方的system message: ")
    opponent_desc = input("请输入反对方的描述: ")
    
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
    config_list = [{
        "model": CUSTOM_LLM_MODEL,
        "api_key": CUSTOM_LLM_API_KEY,
        "base_url": CUSTOM_LLM_API_BASE
    }]

    # 创建支持方智能体
    supporter_agent = ConversableAgent(
        name="supporter",
        system_message=f"""你是支持方辩手。{supporter_system}
        请注意：
        1. 每次发言要有实质性内容，不能返回空消息
        2. 要针对具体论点进行辩论
        3. 使用数据和案例支持你的观点""",
        llm_config={"config_list": config_list},
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
        llm_config={"config_list": config_list},
        human_input_mode="NEVER",
    )

    # 设置智能体描述
    supporter_agent.description = supporter_desc
    opponent_agent.description = opponent_desc
    
    return supporter_agent, opponent_agent, agent_configs

def create_judge_agent():
    """
    创建使用自定义LLM的裁判智能体
    """
    judge_config = [{
        "model": CUSTOM_LLM_MODEL,
        "api_key": CUSTOM_LLM_API_KEY,
        "base_url": CUSTOM_LLM_API_BASE
    }]

    judge_agent = ConversableAgent(
        name="judge_Agent",
        system_message="""你是一个中文辩论赛的裁判。你的任务是：
        1. 用中文引导辩论双方进行讨论
        2. 确保双方发言都有实质性内容
        3. 如果发现某方发言内容为空或无意义，要提醒他重新发言
        4. 仔细倾听双方的论点
        5. 基于论点的说服力和论证的完整性来评判胜者
        6. 当你认为辩论已经充分展开且可以做出判断时，你必须：
           - 说出"辩论结束！"
           - 用中文详细说明判决理由
           - 宣布获胜方
        注意：辩论必须在你说出"辩论结束！"并宣布获胜方后才能结束。""",
        llm_config={"config_list": judge_config},
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: "辩论结束！" in msg["content"],
    )
    
    judge_agent.description = "辩论赛裁判，负责主持辩论并最终决定胜者。"
    return judge_agent

def main():
    """
    主函数
    """
    print("=== 系统初始化 ===")
    
    # 测试LLM连接
    if not test_llm_connection():
        print("LLM连接测试失败，程序退出。")
        return
    
    # 测试AutoGen配置
    if not test_autogen_config():
        print("AutoGen配置测试失败，程序退出。")
        return
    
    print("\n=== 系统初始化完成，开始配置辩论 ===")
    
    # 获取用户输入
    topic = input("请输入辩论主题: ")
    max_rounds = int(input("请输入最大辩论轮数: "))
    
    # 保存模型配置
    model_configs = {
        "model_name": CUSTOM_LLM_MODEL,
        "base_url": CUSTOM_LLM_API_BASE,
        "api_key": "****"  # 不保存实际的API key
    }
    
    # 创建智能体
    supporter_agent, opponent_agent, agent_configs = create_agents(topic)
    judge_agent = create_judge_agent()
    
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
            "config_list": [{
                "model": CUSTOM_LLM_MODEL,
                "api_key": CUSTOM_LLM_API_KEY,
                "base_url": CUSTOM_LLM_API_BASE
            }]
        },
    )

    print("\n=== 开始辩论 ===")
    
    # 启动辩论
    chat_result = judge_agent.initiate_chat(
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
    save_debate_info(topic, agent_configs, chat_result, max_rounds, model_configs)

if __name__ == "__main__":
    main()
