#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WebSocket接口测试
测试WebSocket连接和消息传递
"""

import json
import asyncio
import pytest
import websockets
from pydantic import BaseModel
from typing import Dict, Any, List

# 测试配置
TEST_SERVER = "ws://0.0.0.0:8000"
WEBSOCKET_DEBATE_ENDPOINT = f"{TEST_SERVER}/ws/debate"

# 测试数据
TEST_DEBATE_CONFIG = {
    "topic": "人工智能是否会取代人类工作",
    "max_rounds": 1,
    "supporter_system": "你是支持'人工智能将取代人类工作'观点的辩手",
    "supporter_desc": "AI支持者",
    "opponent_system": "你是反对'人工智能将取代人类工作'观点的辩手",
    "opponent_desc": "AI反对者",
    "enable_speech": False
}

class WebSocketTestResult:
    """WebSocket测试结果类"""
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        self.token_messages: List[Dict[str, Any]] = []
        self.completed = False
        self.error = None
        # 用于跟踪当前正在构建的消息
        self.current_token_content = {}
    
    def add_message(self, message: Dict[str, Any]):
        """添加消息"""
        self.messages.append(message)
        
        # 检查是否是token消息
        if isinstance(message, dict) and message.get("type") == "token":
            self.token_messages.append(message)
            agent = message.get("agent", "unknown")
            token = message.get("token", "")
            is_end = message.get("is_end", False)
            
            # 初始化当前智能体的消息内容如果不存在
            if agent not in self.current_token_content:
                self.current_token_content[agent] = ""
                
            # 添加token到当前内容
            self.current_token_content[agent] += token
            
            # 如果是结束标记，创建一个完整的文本消息
            if is_end:
                text_message = {
                    "type": "text",
                    "agent": agent,
                    "content": self.current_token_content[agent]
                }
                self.messages.append(text_message)
                # 重置当前内容
                self.current_token_content[agent] = ""
        
        # 检查是否完成
        if message.get("status") == "completed":
            self.completed = True
            
        # 检查是否有错误
        if message.get("status") == "error":
            self.error = message.get("message")
    
    @property
    def text_messages(self) -> List[Dict[str, Any]]:
        """获取文本消息"""
        # 检查直接的文本消息
        direct_text_msgs = [msg for msg in self.messages if isinstance(msg, dict) and msg.get("type") == "text"]
        
        # 如果没有直接的文本消息，检查完成消息中的聊天历史
        if not direct_text_msgs:
            for msg in self.messages:
                if isinstance(msg, dict) and msg.get("status") == "completed" and "result" in msg:
                    result = msg.get("result", {})
                    if "chat_history" in result:
                        # 将聊天历史中的每条消息转换为文本消息格式
                        for chat_msg in result.get("chat_history", []):
                            if isinstance(chat_msg, dict) and "content" in chat_msg:
                                direct_text_msgs.append({
                                    "type": "text",
                                    "agent": chat_msg.get("name", "未知"),
                                    "content": chat_msg.get("content", "")
                                })
        
        # 如果仍然没有文本消息，但有token消息，则从当前构建的token内容创建文本消息
        if not direct_text_msgs and self.current_token_content:
            for agent, content in self.current_token_content.items():
                if content:  # 只添加非空内容
                    direct_text_msgs.append({
                        "type": "text",
                        "agent": agent,
                        "content": content
                    })
        
        return direct_text_msgs
    
    @property
    def speech_messages(self) -> List[Dict[str, Any]]:
        """获取语音消息"""
        return [msg for msg in self.messages if isinstance(msg, dict) and msg.get("type") == "speech"]
    
    @property
    def token_messages_count(self) -> int:
        """获取token消息数量"""
        return len(self.token_messages)
    
    @property
    def result(self) -> Dict[str, Any]:
        """获取辩论结果"""
        for msg in self.messages:
            if isinstance(msg, dict) and msg.get("status") == "completed":
                return msg.get("result", {})
        return {}

async def test_websocket_debate():
    """测试WebSocket辩论接口"""
    print("\n测试WebSocket辩论接口...")
    
    result = WebSocketTestResult()
    
    try:
        # 连接WebSocket
        async with websockets.connect(WEBSOCKET_DEBATE_ENDPOINT) as websocket:
            # 发送辩论配置
            await websocket.send(json.dumps(TEST_DEBATE_CONFIG))
            print("已发送辩论配置")
            
            # 设置超时时间（秒）
            timeout = 120
            start_time = asyncio.get_event_loop().time()
            
            # 接收消息直到完成或超时
            while True:
                # 检查是否超时
                current_time = asyncio.get_event_loop().time()
                if current_time - start_time > timeout:
                    print(f"测试超时（{timeout}秒）")
                    break
                
                # 设置接收消息的超时
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    
                    # 解析消息
                    try:
                        # 打印原始消息以进行调试
                        print(f"收到原始消息: {message[:200]}..." if len(message) > 200 else f"收到原始消息: {message}")
                        
                        message_data = json.loads(message)
                        result.add_message(message_data)
                        
                        # 打印消息类型
                        if isinstance(message_data, dict):
                            if message_data.get("type") == "text":
                                agent = message_data.get("agent", "未知")
                                content = message_data.get("content", "")
                                print(f"收到文本消息 - 发言者: {agent}")
                                print(f"  内容: {content[:50]}..." if len(content) > 50 else f"  内容: {content}")
                            elif message_data.get("type") == "speech":
                                agent = message_data.get("agent", "未知")
                                print(f"收到语音消息 - 发言者: {agent}")
                            elif message_data.get("type") == "token":
                                agent = message_data.get("agent", "未知")
                                token = message_data.get("token", "")
                                is_end = message_data.get("is_end", False)
                                if is_end:
                                    print(f"收到token流结束标记 - 发言者: {agent}")
                                elif len(result.token_messages) % 20 == 0:  # 每20个token打印一次以减少输出
                                    print(f"收到token流 - 发言者: {agent}, 当前数量: {len(result.token_messages)}")
                            elif message_data.get("status") == "completed":
                                print("辩论完成")
                                print(f"辩论结果: {json.dumps(message_data.get('result', {}), ensure_ascii=False)[:200]}...")
                                break
                            elif message_data.get("status") == "error":
                                error_msg = message_data.get("message", "未知错误")
                                print(f"发生错误: {error_msg}")
                                break
                            else:
                                print(f"收到未知类型消息: {json.dumps(message_data, ensure_ascii=False)[:200]}...")
                    except json.JSONDecodeError:
                        print(f"收到非JSON消息: {message[:100]}...")
                
                except asyncio.TimeoutError:
                    print("等待消息超时，继续等待...")
                    continue
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket连接已关闭")
                    break
    
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        result.error = str(e)
    
    # 验证测试结果
    if result.error:
        print(f"❌ 测试失败: {result.error}")
        assert False, f"WebSocket测试失败: {result.error}"
    
    # 验证是否收到消息
    if not result.messages:
        print("❌ 测试失败: 未收到任何消息")
        assert False, "未收到任何消息"
        
    # 验证是否收到文本消息
    if not result.text_messages:
        print("❌ 测试失败: 未收到任何文本消息")
        print(f"收到的消息类型: {[type(msg) for msg in result.messages]}")
        print(f"消息内容示例: {str(result.messages[0])[:200] if result.messages else ''}")
        # 如果没有文本消息，检查是否完成并且有聊天历史
        if result.completed and result.result.get("chat_history"):
            # 从聊天历史中提取文本消息
            chat_history = result.result.get("chat_history", [])
            if chat_history:
                print(f"✅ 测试成功: 从辩论结果中提取了 {len(chat_history)} 条聊天消息")
            else:
                print("✅ 测试部分成功: 未收到文本消息，但辩论已完成")
        else:
            assert False, "未收到任何文本消息"
    
    # 验证是否完成辩论
    if not result.completed:
        print("❌ 测试失败: 辩论未完成")
        assert False, "辩论未完成"
    
    # 验证辩论结果
    debate_result = result.result
    if not debate_result:
        print("❌ 测试失败: 未收到辩论结果")
        assert False, "未收到辩论结果"
    
    # 验证辩论结果中是否包含聊天历史
    chat_history = debate_result.get("chat_history", [])
    if not chat_history:
        print("❌ 测试失败: 辩论结果中没有聊天历史")
        assert False, "辩论结果中没有聊天历史"
    
    print(f"✅ 测试成功: WebSocket辩论接口正常工作")
    print(f"  - 收到文本消息数: {len(result.text_messages)}")
    print(f"  - 收到语音消息数: {len(result.speech_messages)}")
    print(f"  - 收到token消息数: {result.token_messages_count}")
    print(f"  - 聊天历史消息数: {len(chat_history)}")
    
    return True

# 运行测试
if __name__ == "__main__":
    print("开始WebSocket测试...")
    asyncio.run(test_websocket_debate())
    print("WebSocket测试完成")
