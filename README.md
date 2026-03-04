# AI辩论代理系统 (AI Agent Debate System)

基于AutoGen框架的多智能体辩论系统，支持自定义主题的结构化辩论，使用DeepSeek模型和SiliconFlow语音服务。

[English Version](README_en.md)

## 功能特点

- 支持自定义辩论主题
- 多智能体交互（支持方、反对方、裁判）
- 结构化辩论流程
- 自动保存辩论记录
- 使用DeepSeek大语言模型
- SiliconFlow语音合成支持
- 中文交互界面
- API接口支持，可用于构建辩论应用
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

1. 启动API服务：
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

## 配置说明

### 环境变量

- `CUSTOM_LLM_API_KEY`: DeepSeek API密钥
- `CUSTOM_LLM_API_BASE`: DeepSeek API基础URL
- `CUSTOM_LLM_MODEL`: DeepSeek模型名称
- `SPEECH_API_KEY`: SiliconFlow API密钥（默认使用`CUSTOM_LLM_API_KEY`）
- `SPEECH_API_BASE`: SiliconFlow API基础URL（默认为`https://api.siliconflow.cn/v1`）
- `SPEECH_MODEL`: SiliconFlow语音模型（默认为`FunAudioLLM/CosyVoice2-0.5B`）

### 自定义设置

- 可以修改main.py中的system message来自定义智能体的行为
- 可以调整最大辩论轮数
- 可以自定义保存的信息格式

## 项目结构

```
.
├─ main.py                # 主程序
├─ server.py              # API服务器
├─ requirements.txt       # 依赖列表
├─ .env.sample           # 环境变量模板
├─ .gitignore            # Git忽略配置
├─ README.md             # 中文文档
├─ README_en.md          # 英文文档
├─ debates/              # 辩论记录保存目录
├─ speech_output/        # 语音输出保存目录
└─ api/                  # API模块
    ├─ agents.py         # 智能体实现
    ├─ config.py         # 配置模块
    ├─ debate.py         # 辩论逻辑
    ├─ models.py         # 数据模型
    ├─ routes.py         # API路由
    ├─ speech.py         # 语音服务
    └─ websocket.py      # WebSocket实现
```

## 注意事项

- 请确保API密钥的安全性
- 建议使用虚拟环境运行程序
- 辩论记录和语音文件会占用磁盘空间，请定期清理
- 如遇到API错误，请检查网络连接和密钥有效性
- 系统默认使用DeepSeek模型和SiliconFlow语音服务，请确保相关API密钥有效

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。在提交代码前，请确保：

1. 代码符合Python代码规范
2. 添加了必要的注释
3. 更新了相关文档
4. 测试通过

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系项目维护者。
