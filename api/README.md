# 辩论系统API

这是一个基于AutoGen框架的多智能体辩论系统API，提供了HTTP和WebSocket接口，可用于构建辩论应用程序。支持文本和语音输出，实时逐字推送。系统使用FastAPI构建，支持同步和异步两种方式进行辩论。系统默认使用DeepSeek大语言模型和SiliconFlow语音合成服务。

## 目录结构

```text
api/
├── __init__.py     # 包初始化文件
├── agents.py       # 智能体模块，处理智能体的创建和交互
├── config.py       # 配置模块，处理环境变量和配置信息
├── debate.py       # 辩论模块，处理辩论的启动和管理
├── models.py       # 数据模型模块，定义API使用的数据模型
├── routes.py       # 路由模块，定义API路由
├── speech.py       # 语音模块，处理文本到语音的转换
└── websocket.py    # WebSocket模块，处理WebSocket连接和消息传递
```

## 使用方法

### 启动服务器

```bash
python server.py
```

服务器将在 http://0.0.0.0:8000 上运行。

### HTTP API

#### 根路由

```http
GET /
```

返回欢迎信息。

**响应示例：**

```json
{
  "message": "欢迎使用辩论系统API"
}
```

#### 测试连接

```http
GET /test_connection
```

测试与DeepSeek LLM的连接状态。

**响应示例：**

```json
{
  "success": true,
  "message": "LLM连接测试成功"
}
```

#### 启动辩论

```http
POST /debate
```

同步启动一场辩论，等待辩论完成后返回完整结果。

**请求参数：**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| topic | string | 是 | 辩论主题 |
| max_rounds | integer | 是 | 最大辩论轮数 |
| supporter_system | string | 是 | 支持方系统提示 |
| supporter_desc | string | 是 | 支持方立场描述 |
| opponent_system | string | 是 | 反对方系统提示 |
| opponent_desc | string | 是 | 反对方立场描述 |
| enable_speech | boolean | 否 | 是否启用语音（默认：true） |

**请求体示例：**

```json
{
  "topic": "买电车还是油车",
  "max_rounds": 20,
  "supporter_system": "激进型辩手",
  "supporter_desc": "买电车",
  "opponent_system": "保守型辩手",
  "opponent_desc": "买油车",
  "enable_speech": true
}
```

**响应示例：**

```json
{
  "topic": "买电车还是油车",
  "max_rounds": 20,
  "chat_history": [
    {
      "name": "裁判",
      "content": "这场关于'买电车还是油车'的辩论现在开始...",
      "role": "judge"
    },
    {
      "name": "支持方",
      "content": "电动汽车代表着未来的出行方式...",
      "role": "supporter"
    },
    // 更多辩论内容...
  ],
  "files": {
    "json_file": "debates/debate_20250427_183500.json",
    "chat_file": "debates/debate_20250427_183500_chat.txt"
  }
}
```

返回辩论结果，包括辩论历史和保存的文件路径。

#### 文本转语音

```http
POST /text_to_speech
```

将文本转换为语音，返回完整的音频数据。

**请求参数：**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| text | string | 是 | 要转换为语音的文本 |
| agent_name | string | 是 | 智能体名称，用于选择声音（supporter/opponent/judge） |

**请求体示例：**

```json
{
  "text": "要转换为语音的文本",
  "agent_name": "supporter"
}
```

**响应示例：**

```json
{
  "file_path": "/path/to/speech_output/12345678-abcd-1234-5678-abcdef123456.mp3",
  "file_id": "12345678-abcd-1234-5678-abcdef123456",
  "audio_base64": "base64编码的音频数据..."
}
```

如果发生错误：

```json
{
  "error": "语音生成失败的错误信息"
}
```

#### 生成语音分块

```http
POST /generate_speech_chunks
```

将长文本分段转换为多个语音片段，适用于实时朗读长文本。

**请求参数：**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| text | string | 是 | 要转换为语音的长文本 |
| agent_name | string | 是 | 智能体名称，用于选择声音（supporter/opponent/judge） |
| chunk_size | integer | 否 | 每个分段的最大字符数（默认：100） |

**请求体示例：**

```json
{
  "text": "要转换为语音的长文本",
  "agent_name": "supporter",
  "chunk_size": 100
}
```

**响应示例：**

```json
{
  "chunks": [
    {
      "file_path": "/path/to/speech_output/chunk1.mp3",
      "file_id": "12345678-abcd-1234-5678-abcdef123456",
      "audio_base64": "base64编码的音频数据..."
    },
    {
      "file_path": "/path/to/speech_output/chunk2.mp3",
      "file_id": "87654321-dcba-4321-8765-fedcba654321",
      "audio_base64": "base64编码的音频数据..."
    }
    // 更多分块...
  ],
  "file_id": "main-file-id",
  "total_chunks": 2
}
```

如果发生错误：

```json
{
  "error": "语音生成失败的错误信息"
}
```

### WebSocket API

#### 辩论WebSocket

```http
ws://localhost:8000/ws/debate
```

通过WebSocket启动一场辩论，实时返回辩论内容和语音数据，支持逐字符流式输出。

**连接流程：**

1. 建立WebSocket连接
2. 发送辩论配置（JSON格式，与HTTP API的`/debate`接口相同格式）
3. 接收实时推送的消息，包括文本、语音和逐字符token消息
4. 辩论结束后接收完成消息

**发送配置示例：**

```json
{
  "topic": "买电车还是油车",
  "max_rounds": 20,
  "supporter_system": "激进型辩手",
  "supporter_desc": "买电车",
  "opponent_system": "保守型辩手",
  "opponent_desc": "买油车",
  "enable_speech": true
}
```

**接收消息类型：**

1. 文本消息：实时推送辩手输出的文本内容

   ```json
   {
     "type": "text",
     "agent": "supporter",
     "content": "辩手输出的文本"
   }
   ```

2. 语音消息：实时推送生成的语音数据

   ```json
   {
     "type": "speech",
     "agent": "supporter",
     "content": "辩手输出的文本",
     "speech": {
       "file_path": "/path/to/audio.mp3",
       "file_id": "unique-id",
       "audio_base64": "base64编码的音频数据"
     }
   }
   ```

3. Token消息：逐字符流式推送辩手输出

   ```json
   {
     "type": "token",
     "agent": "supporter",
     "token": "单个字符或token",
     "is_end": false
   }
   ```
   
   当is_end为true时，表示当前消息的token流已结束：
   
   ```json
   {
     "type": "token",
     "agent": "supporter",
     "token": {"finish_reason": "stop", "text": ""},
     "is_end": true
   }
   ```

3. 完成消息：辩论结束时发送

   ```json
   {
     "status": "completed",
     "result": {
       "topic": "买电车还是油车",
       "max_rounds": 20,
       "chat_history": [...],
       "files": {...}
     }
   }
   ```

4. 错误消息：发生错误时发送

   ```json
   {
     "status": "error",
     "message": "错误信息"
   }
   ```

## 语音功能配置

系统使用SiliconFlow语音服务，可以通过环境变量进行配置，主要配置项如下：

| 环境变量 | 说明 | 默认值 |
| --- | --- | --- |
| `SPEECH_ENABLED` | 是否启用语音功能 | `true` |
| `SPEECH_API_TYPE` | 语音API类型 | `siliconflow` |
| `SPEECH_API_KEY` | SiliconFlow API密钥 | 默认使用`CUSTOM_LLM_API_KEY` |
| `SPEECH_API_BASE` | SiliconFlow API基础URL | `https://api.siliconflow.cn/v1` |
| `SPEECH_MODEL` | SiliconFlow语音模型 | `FunAudioLLM/CosyVoice2-0.5B` |
| `SPEECH_CHUNK_SIZE` | 默认分块大小 | `100` |
| `SPEECH_CACHE_ENABLED` | 是否启用语音缓存 | `true` |

每个智能体的语音可以单独配置：

| 环境变量 | 说明 |
| --- | --- |
| `SUPPORTER_VOICE` | 支持方语音声音（默认：alex） |
| `OPPONENT_VOICE` | 反对方语音声音（默认：alex） |
| `JUDGE_VOICE` | 裁判语音声音（默认：alex） |

## 开发说明

### 添加新功能

1. 在适当的模块中添加新功能
2. 在 `routes.py` 中添加新的路由
3. 如果需要，更新数据模型和配置

### 自定义智能体

在 `agents.py` 中修改智能体的创建和交互逻辑。主要函数：

- `create_agents()`: 创建支持方和反对方智能体
- `create_judge_agent()`: 创建裁判智能体
- `test_llm_connection()`: 测试LLM连接

### 自定义辩论流程

在 `debate.py` 中修改辩论的启动和管理逻辑。主要函数：

- `start_debate()`: 启动辩论，支持同步和异步两种方式
- `save_debate_info()`: 保存辩论信息到文件

### 自定义语音功能

在 `speech.py` 中修改语音生成和处理逻辑。系统使用SiliconFlow语音服务进行语音合成。主要方法：

- `SpeechService.text_to_speech()`: 将文本转换为语音，使用SiliconFlow API
- `SpeechService.generate_speech_chunks()`: 将长文本分段转换为语音

### 数据模型说明

在 `models.py` 中定义了API使用的数据模型：

- `DebateConfig`: 辩论配置模型
- `AgentMessage`: 智能体消息模型
- `SpeechChunk`: 语音分块模型
- `SpeechResult`: 语音生成结果模型
- `DebateResult`: 辩论结果模型
- `WebSocketTextMessage`: 文本消息模型
- `WebSocketSpeechMessage`: 语音消息模型
- `WebSocketTokenMessage`: Token流式消息模型
- `WebSocketMessage`: 消息模型
- `WebSocketResponse`: 响应模型

### 配置说明

在 `config.py` 中定义了系统配置，可通过环境变量进行自定义。系统默认使用DeepSeek大语言模型和SiliconFlow语音服务，相关配置可在`.env`文件中设置。
