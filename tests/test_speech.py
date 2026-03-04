#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试语音API
"""

import asyncio
import sys
import os
import json

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.speech import speech_service
from api.config import SPEECH_API_TYPE, SPEECH_OUTPUT_DIR


async def test_text_to_speech():
    """测试文本转语音功能"""
    print(f"正在测试{SPEECH_API_TYPE}语音API...")
    
    # 测试文本
    test_text = "这是一个测试文本，用于测试语音生成功能。"
    
    # 测试不同角色的语音生成
    for agent_name in ["supporter", "opponent", "judge"]:
        print(f"测试{agent_name}角色的语音生成...")
        
        result = await speech_service.text_to_speech(test_text, agent_name)
        
        if "error" in result:
            print(f"❌ {agent_name}语音生成失败: {result['error']}")
        else:
            print(f"✅ {agent_name}语音生成成功")
            print(f"  - 文件路径: {result['file_path']}")
            print(f"  - 文件ID: {result['file_id']}")
            print(f"  - 音频大小: {len(result['audio_base64']) // 1024} KB")
    
    return True


async def test_generate_speech_chunks():
    """测试长文本分段转语音功能"""
    print(f"\n正在测试{SPEECH_API_TYPE}长文本分段语音生成...")
    
    # 长测试文本
    long_text = """
    人工智能（AI）正在改变我们的生活方式。从智能手机上的语音助手，到自动驾驶汽车，
    再到医疗诊断和金融分析，AI技术已经渗透到各个领域。
    
    深度学习是AI的一个重要分支，它通过模拟人脑的神经网络结构，
    使计算机能够从大量数据中学习和识别模式。这种技术使得机器能够执行复杂的任务，
    如图像识别、自然语言处理和决策制定。
    
    然而，AI的发展也带来了一系列的挑战和伦理问题。我们需要思考如何确保AI技术的公平性、
    透明度和问责制，以及如何保护个人隐私和数据安全。
    
    未来，随着技术的不断进步，AI将继续深入影响我们的社会和经济结构，
    创造新的就业机会，同时也可能取代一些传统工作。
    我们需要积极适应这些变化，培养新的技能，迎接AI时代的挑战和机遇。
    """
    
    # 测试不同角色的长文本语音生成
    agent_name = "supporter"  # 只测试一个角色以节省时间
    chunk_size = 50  # 设置较小的分块大小以便测试
    
    print(f"测试{agent_name}角色的长文本分段语音生成...")
    
    result = await speech_service.generate_speech_chunks(long_text, agent_name, chunk_size)
    
    if "error" in result:
        print(f"❌ 长文本分段语音生成失败: {result['error']}")
        return False
    
    print(f"✅ 长文本分段语音生成成功")
    print(f"  - 总分块数: {result['total_chunks']}")
    print(f"  - 文件ID: {result['file_id']}")
    
    # 打印前两个分块的信息（如果有）
    chunks = result.get("chunks", [])
    for i, chunk in enumerate(chunks[:2]):
        print(f"  - 分块 {i+1}:")
        print(f"    - 文件路径: {chunk['file_path']}")
        print(f"    - 文件ID: {chunk['file_id']}")
        print(f"    - 音频大小: {len(chunk['audio_base64']) // 1024} KB")
    
    if len(chunks) > 2:
        print(f"  - ... 还有 {len(chunks) - 2} 个分块")
    
    return True


async def run_all_tests():
    """运行所有测试"""
    # 确保输出目录存在
    os.makedirs(SPEECH_OUTPUT_DIR, exist_ok=True)
    
    # 打印当前使用的语音API类型
    print(f"当前使用的语音API类型: {SPEECH_API_TYPE}")
    
    # 运行测试
    await test_text_to_speech()
    await test_generate_speech_chunks()
    
    print("\n所有测试完成！")


if __name__ == "__main__":
    # 运行所有测试
    asyncio.run(run_all_tests())
