#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
语音模块
处理文本到语音的转换
"""

import os
import asyncio
import tempfile
import uuid
import base64
import json
from typing import Optional, Dict, Any, List

import aiohttp
from pydub import AudioSegment

from api.config import (SPEECH_OUTPUT_DIR, SPEECH_ENABLED, SPEECH_API_TYPE,
                        SPEECH_API_KEY, SPEECH_API_BASE, SPEECH_DEFAULT_MODEL,
                        SPEECH_DEFAULT_VOICE, SPEECH_SAMPLE_RATE, SPEECH_CACHE_ENABLED,
                        SPEECH_DEFAULT_CHUNK_SIZE)
from api.models import SpeechChunk, SpeechResult

# 确保输出目录存在
os.makedirs(SPEECH_OUTPUT_DIR, exist_ok=True)

class SpeechService:
    """语音服务类，提供文本到语音的转换功能"""
    
    def __init__(self):
        """初始化语音服务"""
        # SiliconFlow使用aiohttp直接调用API
        self.client = None
        # SiliconFlow的声音映射
        self.voice_map = {
            "supporter": f"{SPEECH_DEFAULT_MODEL}:alex",  # 支持方
            "opponent": f"{SPEECH_DEFAULT_MODEL}:alex",   # 反对方
            "judge": f"{SPEECH_DEFAULT_MODEL}:alex"       # 裁判
        }
    
    async def text_to_speech(self, text: str, agent_name: str) -> Dict[str, Any]:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            agent_name: 智能体名称，用于选择声音
            
        Returns:
            包含音频文件路径和base64编码的SpeechChunk对象
        """
        if not SPEECH_ENABLED:
            return {"error": "语音功能未启用"}
        
        # 获取语音配置
        from api.config import SPEECH_CONFIG
        agent_config = SPEECH_CONFIG.get(agent_name, SPEECH_CONFIG.get("supporter"))
        
        # 选择声音和模型
        # SiliconFlow API使用全局默认模型
        model = SPEECH_DEFAULT_MODEL
        # 获取声音配置，但不使用模型前缀
        base_voice = agent_config.get("voice", "alex")
        # 如果声音已经包含完整格式，则直接使用
        if ":" in base_voice:
            voice = base_voice
        else:
            # 否则添加模型前缀
            voice = f"{model}:{base_voice}"
        
        speed = agent_config.get("speed", 1.0)
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        output_path = os.path.join(SPEECH_OUTPUT_DIR, f"{file_id}.mp3")
        
        # 检查缓存（如果启用）
        if SPEECH_CACHE_ENABLED:
            cache_key = f"{agent_name}_{voice}_{model}_{speed}_{text}"
            cache_path = os.path.join(SPEECH_OUTPUT_DIR, f"cache_{hash(cache_key)}.mp3")
            
            if os.path.exists(cache_path):
                # 使用缓存的语音文件
                import shutil
                shutil.copy2(cache_path, output_path)
                
                # 读取文件并转换为base64
                with open(output_path, "rb") as audio_file:
                    audio_data = audio_file.read()
                    audio_base64 = base64.b64encode(audio_data).decode("utf-8")
                
                # 创建并返回SpeechChunk对象
                speech_chunk = SpeechChunk(
                    file_path=output_path,
                    file_id=file_id,
                    audio_base64=audio_base64
                )
                
                return speech_chunk.dict()
        
        try:
            # 使用SiliconFlow API生成语音
            headers = {
                "Authorization": f"Bearer {SPEECH_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # 使用完整的voice格式，如果不包含冒号，则添加模型前缀
            if ":" not in voice:
                voice = f"{model}:{voice}"
            
            data = {
                "model": model,
                "input": text,
                "voice": voice,  # 使用完整的voice格式
                "response_format": "mp3",
                "sample_rate": SPEECH_SAMPLE_RATE,
                "stream": False,  # 测试中使用False，避免流式传输的复杂性
                "speed": speed,
                "gain": 0
            }
            
            # 调试信息
            print(f"调试信息 - SiliconFlow API请求数据:")
            print(f"  - URL: {SPEECH_API_BASE}/audio/speech")
            print(f"  - 模型: {model}")
            print(f"  - 声音: {voice}")
            print(f"  - 采样率: {SPEECH_SAMPLE_RATE}")
            print(f"  - 完整请求数据: {json.dumps(data, ensure_ascii=False)}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{SPEECH_API_BASE}/audio/speech",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        # 保存音频文件
                        with open(output_path, "wb") as f:
                            f.write(await response.read())
                    else:
                        error_text = await response.text()
                        raise Exception(f"SiliconFlow API错误: {error_text}")
            
            # 如果启用缓存，保存副本
            if SPEECH_CACHE_ENABLED:
                import shutil
                shutil.copy2(output_path, cache_path)
            
            # 读取文件并转换为base64
            with open(output_path, "rb") as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode("utf-8")
            
            # 创建并返回SpeechChunk对象
            speech_chunk = SpeechChunk(
                file_path=output_path,
                file_id=file_id,
                audio_base64=audio_base64
            )
            
            return speech_chunk.dict()
        except Exception as e:
            print(f"语音生成失败: {str(e)}")
            return {
                "error": str(e)
            }
    
    async def generate_speech_chunks(self, text: str, agent_name: str, chunk_size: int = None) -> Dict[str, Any]:
        """
        将长文本分段转换为语音，适用于实时朗读
        
        Args:
            text: 要转换的文本
            agent_name: 智能体名称，用于选择声音
            chunk_size: 每个分段的最大字符数，如果为None则使用配置文件中的设置
            
        Returns:
            SpeechResult对象，包含所有生成的语音分块
        """
        if not SPEECH_ENABLED:
            return {"error": "语音功能未启用"}
            
        # 获取语音配置
        from api.config import SPEECH_CONFIG, SPEECH_DEFAULT_CHUNK_SIZE
        agent_config = SPEECH_CONFIG.get(agent_name, SPEECH_CONFIG.get("supporter"))
        
        # 如果没有指定分块大小，使用配置文件中的设置
        if chunk_size is None:
            chunk_size = agent_config.get("chunk_size", SPEECH_DEFAULT_CHUNK_SIZE)
            
        # 分段处理文本
        text_chunks = []
        
        # 如果文本很短，直接作为一个分块
        if len(text) <= chunk_size:
            text_chunks = [text]
        else:
            # 尝试在句子结尾处分割，以保持自然的语音效果
            sentence_endings = ['.', '!', '?', '。', '！', '？', '\n']
            current_chunk = ""
            
            for char in text:
                current_chunk += char
                
                # 如果当前分块达到或超过指定大小，并且当前字符是句子结尾，则分割
                if len(current_chunk) >= chunk_size and char in sentence_endings:
                    text_chunks.append(current_chunk)
                    current_chunk = ""
            
            # 添加最后一个分块（如果有）
            if current_chunk:
                text_chunks.append(current_chunk)
                
            # 如果没有找到合适的分割点，则强制按照字符数分割
            if not text_chunks:
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i+chunk_size]
                    if chunk:
                        text_chunks.append(chunk)
        
        # 生成唯一文件ID
        file_id = str(uuid.uuid4())
        
        # 为每个分段生成语音
        speech_chunks = []
        for i, chunk in enumerate(text_chunks):
            chunk_result = await self.text_to_speech(chunk, agent_name)
            if "error" not in chunk_result:
                # 如果返回的是字典，转换为SpeechChunk对象
                if isinstance(chunk_result, dict):
                    speech_chunk = SpeechChunk(**chunk_result)
                    speech_chunks.append(speech_chunk)
                else:
                    speech_chunks.append(chunk_result)
        
        # 创建并返回SpeechResult对象
        result = SpeechResult(
            chunks=speech_chunks,
            file_id=file_id,
            total_chunks=len(speech_chunks)
        )
        
        return result.dict()

# 创建语音服务实例
speech_service = SpeechService()
