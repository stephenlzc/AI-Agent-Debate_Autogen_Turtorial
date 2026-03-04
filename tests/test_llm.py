#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试LLM API连接
"""

import asyncio
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.agents import test_llm_connection


async def test_deepseek_connection():
    """测试DeepSeek模型连接"""
    print("正在测试DeepSeek模型连接...")
    success, message = await test_llm_connection()
    
    if success:
        print(f"✅ 测试成功: {message}")
    else:
        print(f"❌ 测试失败: {message}")
    
    return success


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_deepseek_connection())
