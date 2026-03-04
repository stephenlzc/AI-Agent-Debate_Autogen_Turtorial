#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试辩论API
"""

import asyncio
import sys
import os
import json
import requests

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.config import SERVER_HOST, SERVER_PORT


def test_root_endpoint():
    """测试根路由"""
    print("测试根路由 GET / ...")
    
    url = f"http://{SERVER_HOST}:{SERVER_PORT}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"✅ 测试成功: 状态码 {response.status_code}")
        print(f"  - 响应内容: {response.json()}")
    else:
        print(f"❌ 测试失败: 状态码 {response.status_code}")
        print(f"  - 错误信息: {response.text}")
    
    return response.status_code == 200


def test_connection_endpoint():
    """测试LLM连接接口"""
    print("\n测试LLM连接 GET /test_connection ...")
    
    url = f"http://{SERVER_HOST}:{SERVER_PORT}/test_connection"
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        success = result.get("success", False)
        message = result.get("message", "")
        
        if success:
            print(f"✅ 测试成功: {message}")
        else:
            print(f"❌ 连接测试失败: {message}")
        
        print(f"  - 响应内容: {result}")
    else:
        print(f"❌ 测试失败: 状态码 {response.status_code}")
        print(f"  - 错误信息: {response.text}")
    
    return response.status_code == 200


def test_text_to_speech_endpoint():
    """测试文本转语音接口"""
    print("\n测试文本转语音 POST /text_to_speech ...")
    
    url = f"http://{SERVER_HOST}:{SERVER_PORT}/text_to_speech"
    data = {
        "text": "这是一个测试文本，用于测试语音API。",
        "agent_name": "supporter"
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        
        if "error" in result:
            print(f"❌ 语音生成失败: {result['error']}")
        else:
            print(f"✅ 测试成功: 语音生成成功")
            print(f"  - 文件ID: {result.get('file_id', 'N/A')}")
            print(f"  - 音频大小: {len(result.get('audio_base64', '')) // 1024} KB")
    else:
        print(f"❌ 测试失败: 状态码 {response.status_code}")
        print(f"  - 错误信息: {response.text}")
    
    return response.status_code == 200


def test_generate_speech_chunks_endpoint():
    """测试生成语音分块接口"""
    print("\n测试生成语音分块 POST /generate_speech_chunks ...")
    
    url = f"http://{SERVER_HOST}:{SERVER_PORT}/generate_speech_chunks"
    data = {
        "text": "这是一个较长的测试文本，用于测试语音分块API。我们将看看系统是否能够正确地将文本分成多个块，并为每个块生成语音。这对于实时朗读长文本非常有用。",
        "agent_name": "supporter",
        "chunk_size": 30
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        
        if "error" in result:
            print(f"❌ 语音分块生成失败: {result['error']}")
        else:
            chunks = result.get("chunks", [])
            print(f"✅ 测试成功: 语音分块生成成功")
            print(f"  - 总分块数: {result.get('total_chunks', 0)}")
            print(f"  - 文件ID: {result.get('file_id', 'N/A')}")
            
            # 打印前两个分块的信息（如果有）
            for i, chunk in enumerate(chunks[:2]):
                print(f"  - 分块 {i+1}:")
                print(f"    - 文件ID: {chunk.get('file_id', 'N/A')}")
                print(f"    - 音频大小: {len(chunk.get('audio_base64', '')) // 1024} KB")
            
            if len(chunks) > 2:
                print(f"  - ... 还有 {len(chunks) - 2} 个分块")
    else:
        print(f"❌ 测试失败: 状态码 {response.status_code}")
        print(f"  - 错误信息: {response.text}")
    
    return response.status_code == 200


def test_debate_endpoint():
    """测试辩论接口（简短版本）"""
    print("\n测试辩论接口 POST /debate (简短版本) ...")
    
    url = f"http://{SERVER_HOST}:{SERVER_PORT}/debate"
    data = {
        "topic": "人工智能是否会取代人类工作",
        "max_rounds": 1,  # 设置为1轮以加快测试速度
        "supporter_system": "技术乐观主义者",
        "supporter_desc": "支持AI将创造更多就业机会",
        "opponent_system": "技术保守主义者",
        "opponent_desc": "担忧AI会导致大规模失业",
        "enable_speech": True
    }
    
    print("正在启动辩论，这可能需要一些时间...")
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        chat_history = result.get("chat_history", [])
        
        print(f"✅ 测试成功: 辩论完成")
        print(f"  - 主题: {result.get('topic', 'N/A')}")
        print(f"  - 轮数: {result.get('max_rounds', 0)}")
        print(f"  - 消息数: {len(chat_history)}")
        
        # 打印前几条消息（如果有）
        for i, msg in enumerate(chat_history[:3]):
            print(f"  - 消息 {i+1}:")
            print(f"    - 发言者: {msg.get('name', 'N/A')}")
            print(f"    - 角色: {msg.get('role', 'N/A')}")
            content = msg.get('content', '')
            print(f"    - 内容: {content[:50]}..." if len(content) > 50 else f"    - 内容: {content}")
        
        if len(chat_history) > 3:
            print(f"  - ... 还有 {len(chat_history) - 3} 条消息")
        
        # 打印保存的文件信息
        files = result.get("files", {})
        if files:
            print("  - 保存的文件:")
            for file_type, file_path in files.items():
                print(f"    - {file_type}: {file_path}")
    else:
        print(f"❌ 测试失败: 状态码 {response.status_code}")
        print(f"  - 错误信息: {response.text}")
    
    return response.status_code == 200


def run_all_tests():
    """运行所有API测试"""
    print(f"开始测试API接口 (服务器: http://{SERVER_HOST}:{SERVER_PORT})")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        requests.get(f"http://{SERVER_HOST}:{SERVER_PORT}/", timeout=5)
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器已启动")
        print(f"  - 服务器地址: http://{SERVER_HOST}:{SERVER_PORT}")
        print("  - 可以通过运行 'python server.py' 启动服务器")
        return False
    
    # 运行测试
    success_count = 0
    total_tests = 5
    
    if test_root_endpoint():
        success_count += 1
    
    if test_connection_endpoint():
        success_count += 1
    
    if test_text_to_speech_endpoint():
        success_count += 1
    
    if test_generate_speech_chunks_endpoint():
        success_count += 1
    
    if test_debate_endpoint():
        success_count += 1
    
    # 打印测试结果摘要
    print("\n" + "=" * 50)
    print(f"测试完成: {success_count}/{total_tests} 个测试通过")
    
    if success_count == total_tests:
        print("✅ 所有测试都通过了！")
    else:
        print(f"❌ {total_tests - success_count} 个测试失败")
    
    return success_count == total_tests


if __name__ == "__main__":
    # 运行所有测试
    run_all_tests()
