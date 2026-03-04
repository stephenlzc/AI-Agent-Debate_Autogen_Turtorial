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
- DeepSeek API密钥
- SiliconFlow API密钥（用于语音合成）

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/FicoHu/AI-Agent-Debate.git
cd AI-Agent-Debate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量：

```bash
cp .env.sample .env
```

然后编辑.env文件，填入你的API密钥和配置信息。

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

2. 使用HTTP API：

   - 测试连接：`GET /test_connection`
   - 启动辩论：`POST /debate`
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

2. 使用Flask API：
   - 获取辩论列表：`GET /api/debates`
   - 获取辩论详情：`GET /api/debate?debate_id=xxx`
   - 创建新辩论：`POST /api/addDebate`
   - 从新闻生成辩论：`POST /api/generate_debate`
   - 生成语音：`POST /api/generate_speech`
   - 生成辩论海报：`GET /api/generate_photo?theme=xxx`
   - 详细API文档见：`flask/api.md`

### 前端界面

1. 安装依赖并启动前端开发服务器：

```bash
cd frontend
npm install
npm run dev
```

2. 构建前端生产版本：

```bash
cd frontend
npm run build
```

3. 前端功能：
   - 登录和注册界面
   - 热点辩论列表
   - 辩论详情页面（支持音频播放）
   - 添加辩论主题
   - 从新闻URL生成辩论
   - 用户个人资料管理

## 配置说明

### 环境变量

- `CUSTOM_LLM_API_KEY`: DeepSeek API密钥
- `CUSTOM_LLM_API_BASE`: DeepSeek API基础URL
- `CUSTOM_LLM_MODEL`: DeepSeek模型名称
- `SPEECH_API_KEY`: SiliconFlow API密钥（默认使用 `CUSTOM_LLM_API_KEY`）
- `SPEECH_API_BASE`: SiliconFlow API基础URL（默认为 `https://api.siliconflow.cn/v1`）
- `SPEECH_MODEL`: SiliconFlow语音模型（默认为 `FunAudioLLM/CosyVoice2-0.5B`）

### 自定义设置

- 可以修改main.py中的system message来自定义智能体的行为
- 可以调整最大辩论轮数
- 可以自定义保存的信息格式

## 项目结构

```
.
├─ main.py                # 主程序
├─ server.py              # AutoGen API服务器
├─ requirements.txt       # 依赖列表
├─ requirements_api.txt   # API服务依赖列表
├─ .env.sample           # 环境变量模板
├─ .env.example          # 环境变量示例
├─ .gitignore            # Git忽略配置
├─ README.md             # 中文文档
├─ Dockerfile            # Docker构建文件
├─ update_and_run.sh     # 更新和运行脚本
├─ monitor.sh            # 监控脚本
├─ debates/              # 辩论记录保存目录
├─ speech_output/        # 语音输出保存目录
├─ audio_output/         # Flask API语音输出目录
├─ debates.jsonl         # 辩论数据存储文件
├─ api/                  # AutoGen API模块
│   ├─ agents.py         # 智能体实现
│   ├─ config.py         # 配置模块
│   ├─ debate.py         # 辩论逻辑
│   ├─ models.py         # 数据模型
│   ├─ routes.py         # API路由
│   ├─ speech.py         # 语音服务
│   └─ websocket.py      # WebSocket实现
├─ flask/                # Flask API服务
│   ├─ app.py            # Flask应用主程序
│   ├─ debates.py        # 辩论管理API
│   ├─ debatefromnews.py # 从新闻生成辩论API
│   ├─ ttv.py            # 文本转语音API
│   ├─ ttv3.py           # 华为云文本转语音API
│   ├─ photo.py          # 图片生成API
│   └─ api.md            # API文档
├─ model/                # 模型相关代码
│   ├─ train.py          # 训练脚本
│   ├─ test_app.py       # 测试应用
│   ├─ data.py           # 数据处理
│   └─ customize_service.py # 自定义服务
├─ tests/                # 测试目录
└─ frontend/             # 前端Vue.js应用
    ├─ package.json      # 前端依赖配置
    ├─ vite.config.js    # Vite配置
    ├─ index.html        # 入口HTML
    ├─ public/           # 静态资源
    └─ src/              # 源代码
        ├─ main.js       # 主入口
        ├─ App.vue       # 根组件
        ├─ assets/       # 资源文件
        ├─ components/   # 公共组件
        ├─ config/       # 配置
        ├─ router/       # 路由
        ├─ store/        # 状态管理
        └─ views/        # 页面组件
            ├─ Login.vue           # 登录页面
            ├─ OtherLogin.vue      # 其他登录方式
            ├─ HotDebates.vue      # 热点辩论列表
            ├─ DebateView.vue      # 辩论详情
            ├─ AddDebateTopic.vue  # 添加辩论主题
            ├─ Discover.vue        # 发现页面
            └─ UserProfile.vue     # 用户资料
```

## 注意事项

- 请确保API密钥的安全性，不要将包含密钥的配置文件提交到公共仓库
- 建议使用虚拟环境运行程序
- 辩论记录和语音文件会占用磁盘空间，请定期清理
- 如遇到API错误，请检查网络连接和密钥有效性
- 系统使用多种外部API服务，包括：
  - DeepSeek大语言模型（用于辩论生成）
  - SiliconFlow语音服务（用于语音合成）
  - 华为云语音合成服务（作为备选语音服务）
  - 火山引擎图像生成服务（用于生成辩论海报）
- 前端开发需要Node.js环境，请确保安装了正确版本
- Flask API和前端需要分别启动，确保端口设置正确以允许跨域请求
