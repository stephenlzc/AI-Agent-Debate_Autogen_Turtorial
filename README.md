# AI辩论代理系统 (AI Agent Debate System)

基于AutoGen框架的多智能体辩论系统，支持自定义主题的结构化辩论，使用DeepSeek模型和SiliconFlow语音服务。系统包含后端API服务(Flask)和前端界面(Vue.js)，支持从新闻生成辩论内容，并提供语音合成和图片生成功能。

## 功能特点

- 支持自定义辩论主题
- 多智能体交互（支持方、反对方、裁判）
- 结构化辩论流程
- 自动保存辩论记录
- 使用DeepSeek大语言模型
- 多种语音合成支持（SiliconFlow和华为云）
- 从新闻URL自动生成辩论内容
- 自动生成辩论海报（使用火山引擎AI服务）
- 现代化Vue.js前端界面，适配移动设备
- 完整的用户系统（登录、注册、个人资料）
- RESTful API接口，支持前后端分离
- WebSocket支持，实时逐字显示辩手输出

## 系统要求

- Python 3.9+
- Node.js 18+ (前端开发)
- 各类API密钥（详见环境变量配置）

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/stephenlzc/AI-Agent-Debate_Autogen_Turtorial.git
cd AI-Agent-Debate_Autogen_Turtorial
```

2. 安装依赖：

```bash
# 基础依赖
pip install -r requirements.txt

# API服务完整依赖（包含FastAPI、异步HTTP等）
pip install -r requirements_api.txt
```

3. 配置环境变量：

```bash
cp .env.sample .env
```

然后编辑 `.env` 文件，填入你的API密钥和配置信息。详见下方【环境变量配置】章节。

## 使用方法

### 命令行模式

1. 启动程序：

```bash
python main.py
```

2. 按提示输入：

   - 辩论主题
   - 最大辩论轮数
   - 支持方和反对方的system message
   - 双方的描述信息
3. 观看辩论进行：

   - 程序会自动进行辩论
   - 裁判会主持和引导讨论
   - 最终会宣布获胜方
4. 查看结果：

   - 辩论记录会自动保存在debates目录下
   - 包含JSON格式的完整记录和易读的文本记录
   - 如果启用了语音功能，语音文件会保存在speech_output目录下

### API模式

1. 启动AutoGen API服务：

```bash
python server.py
```

服务默认运行在 http://localhost:8000

2. 使用HTTP API：

   - 测试连接：`GET /test_connection`
   - 启动辩论：`POST /debate`
   - 文本转语音：`POST /text_to_speech`
3. 使用WebSocket API（逐字输出）：

   - 连接：`ws://localhost:8000/ws/debate`
   - 发送配置信息开始辩论
   - 实时接收辩手输出

### Flask API服务

1. 启动Flask API服务：

```bash
cd flask
python app.py
```

服务默认运行在 http://localhost:9000

2. 使用Flask API：
   - 获取辩论列表：`GET /api/debates`
   - 获取辩论详情：`GET /api/debate?debate_id=xxx`
   - 创建新辩论：`POST /api/addDebate`
   - 从新闻生成辩论：`POST /api/generate_debate`
   - 生成语音：`POST /api/generate_speech`
   - 生成辩论海报：`GET /api/generate_photo?theme=xxx`
   - 详细API文档见：`flask/api.md`

### 前端界面

1. 配置前端环境变量：

```bash
cd frontend
# 创建本地环境配置
echo "VUE_APP_API_URL=http://localhost:9000" > .env.local
```

2. 安装依赖并启动前端开发服务器：

```bash
npm install
npm run dev
```

前端默认运行在 http://localhost:3001

3. 构建前端生产版本：

```bash
npm run build
```

4. 前端功能：
   - 登录和注册界面
   - 热点辩论列表
   - 辩论详情页面（支持音频播放）
   - 添加辩论主题
   - 从新闻URL生成辩论
   - 用户个人资料管理

## 配置说明

### 环境变量

复制 `.env.sample` 为 `.env`，并配置以下变量：

#### 1. DeepSeek LLM API (SiliconFlow平台)

| 变量名 | 说明 | 获取地址 |
|--------|------|----------|
| `CUSTOM_LLM_API_KEY` | DeepSeek API密钥 | https://cloud.siliconflow.cn/ |
| `CUSTOM_LLM_API_BASE` | API基础URL | `https://api.siliconflow.cn/v1` |
| `CUSTOM_LLM_MODEL` | 模型名称 | `deepseek-ai/DeepSeek-V3` |

#### 2. SiliconFlow Speech API (语音合成)

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SPEECH_API_KEY` | 语音API密钥 | 默认使用 `CUSTOM_LLM_API_KEY` |
| `SPEECH_API_BASE` | 语音API基础URL | `https://api.siliconflow.cn/v1` |
| `SPEECH_MODEL` | 语音模型 | `FunAudioLLM/CosyVoice2-0.5B` |
| `SPEECH_VOICE` | 默认语音 | `FunAudioLLM/CosyVoice2-0.5B:alex` |

#### 3. Huawei Cloud AK/SK (备用语音服务)

| 变量名 | 说明 | 获取地址 |
|--------|------|----------|
| `HUAWEI_CLOUD_AK` | 华为云Access Key | https://console.huaweicloud.com/iam/ |
| `HUAWEI_CLOUD_SK` | 华为云Secret Key | https://console.huaweicloud.com/iam/ |

#### 4. Volcano Engine (火山引擎 - AI图片生成)

| 变量名 | 说明 | 获取地址 |
|--------|------|----------|
| `VOLCANO_ACCESS_KEY` | 火山引擎Access Key | https://console.volcengine.com/iam/accesskey/ |
| `VOLCANO_SECRET_KEY` | 火山引擎Secret Key | https://console.volcengine.com/iam/accesskey/ |

#### 5. ModelArts API (新闻生成辩论)

| 变量名 | 说明 | 获取地址 |
|--------|------|----------|
| `MODELARTS_API_KEY` | ModelArts API密钥 | https://console.huaweicloud.com/modelarts/ |

#### 6. 服务器配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SERVER_HOST` | 服务器监听地址 | `0.0.0.0` |
| `SERVER_PORT` | 服务器端口 | `8000` |
| `CORS_ORIGINS` | 允许的跨域来源 | `["http://localhost:3000"]` |
| `FLASK_DEBUG` | Flask调试模式 | `false` |
| `DEBUG` | 全局调试模式 | `false` |

#### 7. 语音服务配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SPEECH_ENABLED` | 是否启用语音 | `true` |
| `SPEECH_API_TYPE` | 语音服务类型 | `siliconflow` |
| `SPEECH_CACHE_ENABLED` | 是否启用缓存 | `true` |
| `SUPPORTER_VOICE` | 支持者音色 | `alloy` |
| `OPPONENT_VOICE` | 反对者音色 | `echo` |
| `JUDGE_VOICE` | 裁判音色 | `onyx` |

### 自定义设置

- 可以修改 `main.py` 中的system message来自定义智能体的行为
- 可以调整最大辩论轮数（通过 `DEFAULT_MAX_ROUNDS` 环境变量）
- 可以自定义保存的信息格式
- 可以配置不同角色的语音参数

## 项目结构

```
.
├─ main.py                # 主程序（命令行模式）
├─ server.py              # FastAPI服务器（WebSocket + REST API）
├─ requirements.txt       # 基础依赖列表
├─ requirements_api.txt   # API服务完整依赖
├─ .env.sample            # 环境变量模板
├─ .env                   # 环境变量配置（不提交到Git）
├─ .gitignore             # Git忽略配置
├─ README.md              # 项目文档
├─ AGENTS.md              # 开发指南（AutoGen配置）
├─ Dockerfile             # Docker构建文件
├─ update_and_run.sh      # 更新和运行脚本
├─ monitor.sh             # 监控脚本
├─ debates/               # 辩论记录保存目录
├─ speech_output/         # FastAPI语音输出目录
├─ audio_output/          # Flask API语音输出目录
├─ debates.jsonl          # 辩论数据存储文件
├─ api/                   # FastAPI模块
│   ├─ agents.py          # 智能体实现
│   ├─ config.py          # 配置模块
│   ├─ debate.py          # 辩论逻辑
│   ├─ models.py          # 数据模型
│   ├─ routes.py          # API路由
│   ├─ speech.py          # 语音服务
│   └─ websocket.py       # WebSocket实现
├─ flask/                 # Flask API服务
│   ├─ app.py             # Flask应用主程序
│   ├─ debates.py         # 辩论管理API
│   ├─ debatefromnews.py  # 从新闻生成辩论API
│   ├─ ttv.py             # 文本转语音API
│   ├─ ttv2.py            # 备用文本转语音API
│   ├─ ttv3.py            # 华为云文本转语音API
│   ├─ photo.py           # 图片生成API
│   └─ api.md             # API详细文档
├─ model/                 # 模型相关代码
│   ├─ train.py           # 训练脚本
│   ├─ test_app.py        # 测试应用
│   ├─ data.py            # 数据处理
│   └─ customize_service.py # 自定义服务
├─ tests/                 # 测试目录
│   ├─ test_debate_api.py
│   ├─ test_websocket.py
│   ├─ test_llm.py
│   ├─ test_speech.py
│   └─ run_tests.py
└─ frontend/              # 前端Vue.js应用
    ├─ package.json       # 前端依赖配置
    ├─ vite.config.js     # Vite配置
    ├─ index.html         # 入口HTML
    ├─ .env.local         # 前端本地环境配置
    ├─ public/            # 静态资源
    └─ src/               # 源代码
        ├─ main.js        # 主入口
        ├─ App.vue        # 根组件
        ├─ assets/        # 资源文件
        ├─ components/    # 公共组件
        ├─ config/        # 配置
        ├─ router/        # 路由
        ├─ views/         # 页面组件
        └─ ...
```

## 安全注意事项

⚠️ **重要安全提示**：

1. **保护API密钥**
   - 永远不要将 `.env` 文件提交到Git仓库
   - 定期轮换API密钥
   - 在生产环境使用最小权限原则

2. **CORS配置**
   - 生产环境请限制 `CORS_ORIGINS` 为具体域名
   - 默认配置仅允许本地开发环境

3. **调试模式**
   - 生产环境必须设置 `FLASK_DEBUG=false` 和 `DEBUG=false`
   - 调试模式会暴露敏感信息

4. **路径安全**
   - 系统已添加路径遍历防护
   - 不要手动修改 `audio_output` 目录权限

5. **外部服务**
   - 系统使用多种外部API服务，请注意费用控制
   - 建议配置API使用限额

## 更新日志

### 2025-03-04 安全更新

- ✅ 移除所有硬编码API密钥，改为环境变量配置
- ✅ 修复路径遍历漏洞
- ✅ 限制CORS默认只允许本地开发
- ✅ 添加所有HTTP请求超时设置
- ✅ 修复WebSocket错误信息泄露
- ✅ 添加线程锁保护debates.jsonl文件操作
- ✅ 修复前端内存泄漏和硬编码IP
- ✅ 更新依赖列表，补充缺失包
- ✅ 完善环境变量配置文档

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

[MIT](LICENSE)

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
