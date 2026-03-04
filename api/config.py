#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置模块
处理环境变量和配置信息
"""

import os
import json
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# API密钥配置
CUSTOM_LLM_API_KEY = os.getenv('CUSTOM_LLM_API_KEY')
CUSTOM_LLM_API_BASE = os.getenv('CUSTOM_LLM_API_BASE')
CUSTOM_LLM_MODEL = os.getenv('CUSTOM_LLM_MODEL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', CUSTOM_LLM_API_KEY)  # 默认使用自定义LLM的API密钥

# 语音相关配置
SPEECH_ENABLED = os.getenv('SPEECH_ENABLED', 'true').lower() == 'true'
SPEECH_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'speech_output')
SPEECH_API_TYPE = os.getenv('SPEECH_API_TYPE', 'siliconflow')  # 默认使用 siliconflow
SPEECH_API_KEY = os.getenv('SPEECH_API_KEY', CUSTOM_LLM_API_KEY)
SPEECH_API_BASE = os.getenv('SPEECH_API_BASE', 'https://api.siliconflow.cn/v1')
SPEECH_DEFAULT_MODEL = os.getenv('SPEECH_MODEL', 'FunAudioLLM/CosyVoice2-0.5B')
SPEECH_DEFAULT_VOICE = os.getenv('SPEECH_VOICE', 'FunAudioLLM/CosyVoice2-0.5B:alex')
SPEECH_DEFAULT_CHUNK_SIZE = int(os.getenv('SPEECH_CHUNK_SIZE', '100'))
SPEECH_CACHE_ENABLED = os.getenv('SPEECH_CACHE_ENABLED', 'true').lower() == 'true'
SPEECH_SAMPLE_RATE = int(os.getenv('SPEECH_SAMPLE_RATE', '44100'))

# 辩论输出目录
DEBATES_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'debates')
os.makedirs(DEBATES_OUTPUT_DIR, exist_ok=True)
os.makedirs(SPEECH_OUTPUT_DIR, exist_ok=True)

# 检查必要的环境变量
if not all([CUSTOM_LLM_API_KEY, CUSTOM_LLM_API_BASE, CUSTOM_LLM_MODEL]):
    raise ValueError("请确保.env文件中包含所有必要的配置项")

# 默认配置
DEFAULT_CONFIG = {
    "model_name": CUSTOM_LLM_MODEL,
    "base_url": CUSTOM_LLM_API_BASE,
    "api_key": CUSTOM_LLM_API_KEY
}

# 检查是否使用DeepSeek模型
IS_DEEPSEEK_MODEL = 'DeepSeek' in CUSTOM_LLM_MODEL

# LLM配置
LLM_CONFIG = [{
    "model": CUSTOM_LLM_MODEL,
    "api_key": CUSTOM_LLM_API_KEY,
    "base_url": CUSTOM_LLM_API_BASE
    # 注意：temperature和is_deepseek参数不能在这里设置，因为autogen 0.9不支持
    # 这些参数应该在调用OpenAI API时设置
}]

# 语音配置
SPEECH_CONFIG = {
    "supporter": {
        "voice": os.getenv('SUPPORTER_VOICE', 'alloy'),  # 支持方使用alloy声音
        "model": os.getenv('SUPPORTER_TTS_MODEL', 'tts-1'),
        "speed": float(os.getenv('SUPPORTER_SPEED', '1.0')),
        "chunk_size": int(os.getenv('SUPPORTER_CHUNK_SIZE', str(SPEECH_DEFAULT_CHUNK_SIZE)))
    },
    "opponent": {
        "voice": os.getenv('OPPONENT_VOICE', 'echo'),   # 反对方使用echo声音
        "model": os.getenv('OPPONENT_TTS_MODEL', 'tts-1'),
        "speed": float(os.getenv('OPPONENT_SPEED', '1.0')),
        "chunk_size": int(os.getenv('OPPONENT_CHUNK_SIZE', str(SPEECH_DEFAULT_CHUNK_SIZE)))
    },
    "judge": {
        "voice": os.getenv('JUDGE_VOICE', 'onyx'),   # 裁判使用onyx声音
        "model": os.getenv('JUDGE_TTS_MODEL', 'tts-1'),
        "speed": float(os.getenv('JUDGE_SPEED', '1.0')),
        "chunk_size": int(os.getenv('JUDGE_CHUNK_SIZE', str(SPEECH_DEFAULT_CHUNK_SIZE)))
    }
}

# 服务器配置
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
CORS_ORIGINS = json.loads(os.getenv('CORS_ORIGINS', '["*"]'))

# 辩论配置
DEFAULT_MAX_ROUNDS = int(os.getenv('DEFAULT_MAX_ROUNDS', '3'))
