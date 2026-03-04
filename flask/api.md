# AI辩论系统API文档

## 目录
1. [概述](#概述)
2. [辩论管理API](#辩论管理api)
3. [文本转语音API](#文本转语音api)
4. [从新闻生成辩论API](#从新闻生成辩论api)
5. [图片生成API](#图片生成api)
6. [音频文件服务](#音频文件服务)

## 概述

本文档详细描述了AI辩论系统的后端API接口。系统基于Flask框架构建，提供了辩论管理、文本转语音、从新闻生成辩论以及图片生成等功能。所有API均支持跨域请求。

服务器默认运行在`0.0.0.0:9000`，开启了调试模式。

## 辩论管理API

### 获取辩论列表

- **URL**: `/api/debates`
- **方法**: `GET`
- **描述**: 获取辩论列表，支持分页、状态过滤和搜索
- **参数**:
  - `page`: 页码，默认为1
  - `per_page`: 每页条数，默认为10
  - `status`: 状态过滤，可选值有upcoming、ongoing等
  - `search`: 搜索关键词，将在主题和队伍名称中搜索
- **响应示例**:
```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "total": 10,
    "page": 1,
    "per_page": 10,
    "debates": [
      {
        "id": "abc",
        "topic": "人工智能利大于弊还是弊大于利",
        "url": "https://example.com/article",
        "pros": {
          "team": "创新者联盟",
          "argument": "AI将推动社会生产力革命性提升"
        },
        "cons": {
          "team": "人文守护者",
          "argument": "AI可能导致大规模失业和社会分化"
        },
        "poster": "https://example.com/posters/ai_debate.jpg",
        "schedule": {
          "time": "2024-03-15 19:00",
          "location": "线上直播厅A"
        },
        "status": "upcoming",
        "view_count": 0,
        "created_at": "2024-05-06T09:30:00"
      }
    ]
  }
}
```

### 获取辩论详情

- **URL**: `/api/debate`
- **方法**: `GET`
- **描述**: 获取单个辩论的详细信息
- **参数**:
  - `debate_id`: 辩论ID
- **响应示例**:
```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "id": "abc",
    "topic": "人工智能利大于弊还是弊大于利",
    "url": "https://example.com/article",
    "pros": {
      "team": "创新者联盟",
      "argument": "AI将推动社会生产力革命性提升"
    },
    "cons": {
      "team": "人文守护者",
      "argument": "AI可能导致大规模失业和社会分化"
    },
    "poster": "https://example.com/posters/ai_debate.jpg",
    "schedule": {
      "time": "2024-03-15 19:00",
      "location": "线上直播厅A"
    },
    "status": "upcoming",
    "view_count": 1,
    "created_at": "2024-05-06T09:30:00",
    "rounds": [
      {
        "type": "emcee",
        "msg": "主持人话术1",
        "path": "audio_output/audio_12345678.mp3"
      },
      {
        "type": "pro",
        "msg": "正方论点论据1",
        "path": "audio_output/audio_23456789.mp3"
      }
    ]
  }
}
```

### 创建新辩论

- **URL**: `/api/addDebate`
- **方法**: `POST`
- **描述**: 创建新的辩论赛
- **请求体**:
```json
{
  "topic": "辩论主题",
  "url": "https://example.com/article",
  "pros": {
    "team": "正方队伍名称",
    "argument": "正方立场"
  },
  "cons": {
    "team": "反方队伍名称",
    "argument": "反方立场"
  },
  "poster": "https://example.com/posters/debate.jpg",
  "schedule": {
    "time": "2024-05-10 19:00",
    "location": "线上直播厅B"
  },
  "status": "upcoming",
  "rounds": [
    {
      "type": "emcee",
      "msg": "主持人话术"
    },
    {
      "type": "pro",
      "msg": "正方论点"
    }
  ]
}
```
- **响应示例**:
```json
{
  "code": 201,
  "message": "创建成功",
  "data": {
    "debate_id": "def456"
  }
}
```

## 文本转语音API

### 生成语音

- **URL**: `/api/generate_speech`
- **方法**: `POST`
- **描述**: 将文本转换为语音
- **请求体**:
```json
{
  "input": "要转换为语音的文本",
  "voice": "FunAudioLLM/CosyVoice2-0.5B:alex",
  "response_format": "mp3",
  "sample_rate": 32000,
  "stream": true,
  "speed": 1,
  "gain": 0
}
```
- **参数说明**:
  - `input`: 必填，要转换的文本内容
  - `voice`: 可选，声音风格，默认为"FunAudioLLM/CosyVoice2-0.5B:alex"
  - `response_format`: 可选，响应格式，默认为"mp3"
  - `sample_rate`: 可选，采样率，默认为32000Hz
  - `stream`: 可选，是否为流式响应，默认为true
  - `speed`: 可选，生成速度，默认为1倍速
  - `gain`: 可选，音量增益，默认为0
- **响应**: 直接返回音频流数据

## 从新闻生成辩论API

### 从新闻生成辩论

- **URL**: `/api/generate_debate`
- **方法**: `POST`
- **描述**: 从新闻URL生成辩论内容
- **请求体**:
```json
{
  "url": "https://example.com/news-article"
}
```
- **响应**: 返回生成的辩论数据，格式与辩论详情相同，并自动将生成的辩论保存到系统中

## 图片生成API

### 生成辩论海报

- **URL**: `/api/generate_photo`
- **方法**: `GET`
- **描述**: 根据主题生成辩论海报
- **参数**:
  - `theme`: 辩论主题
- **响应示例**:
```json
{
  "data": {
    "image_urls": [
      "https://example.com/generated-poster.jpg"
    ]
  }
}
```

## 音频文件服务

### 获取音频文件

- **URL**: `/audio_output/<filename>`
- **方法**: `GET`
- **描述**: 提供音频文件的访问服务
- **参数**:
  - `filename`: 音频文件名
- **响应**: 直接返回音频文件

### 测试音频目录

- **URL**: `/audio_output/test`
- **方法**: `GET`
- **描述**: 列出音频目录中的所有文件
- **响应示例**:
```json
{
  "files": [
    "audio_12345678.mp3",
    "audio_23456789.mp3"
  ]
}
```

## 技术实现说明

系统使用了多个外部API服务：

1. **文本转语音服务**:
   - 使用华为云语音合成服务
   - 支持多种发音人选择，如chinese_xiaoqi_common、chinese_huaxiaogang_common等

2. **图片生成服务**:
   - 使用火山引擎的图像生成服务
   - 通过提供辩论主题生成相关的辩论海报

3. **辩论生成服务**:
   - 使用DeepSeek-V3模型
   - 从网页内容中提取信息并生成结构化的辩论内容

所有生成的音频文件均保存在项目的`audio_output`目录中，并通过Flask提供文件访问服务。
