# AI Agent Debate System - Agent Guide

## Project Overview

This is an AI Agent Debate System (AI辩论代理系统) built on the AutoGen framework. It supports structured debates on customizable topics using multi-agent interactions with DeepSeek LLM and SiliconFlow speech services.

**Key Capabilities:**
- Multi-agent debate with pro, con, and judge roles
- Real-time WebSocket streaming of debate content
- Text-to-speech synthesis (SiliconFlow primary, Huawei Cloud backup)
- Auto-generation of debates from news URLs
- AI-generated debate posters (Volcano Engine)
- Vue.js frontend with mobile support
- Complete user system (login, profile)

## Technology Stack

### Backend
- **Python 3.9+** - Main language
- **AutoGen 0.9** - Multi-agent conversation framework
- **Flask** - REST API server (port 9000)
- **FastAPI + Uvicorn** - WebSocket/Streaming API (port 8001)
- **OpenAI SDK** - LLM API client
- **aiohttp** - Async HTTP client for speech APIs
- **BeautifulSoup** - Web scraping for news extraction

### Frontend
- **Vue.js 3** - Frontend framework
- **Vite 6.x** - Build tool
- **Vue Router 4.x** - Client-side routing
- **Axios** - HTTP client

### External Services
- **DeepSeek API** - LLM for debate generation
- **SiliconFlow API** - Primary TTS service (CosyVoice2-0.5B)
- **Huawei Cloud** - Backup TTS service
- **Volcano Engine** - Image generation for posters

## Project Structure

```
.
├── main.py                 # CLI entry point (interactive debate)
├── server.py               # FastAPI server entry point
├── requirements.txt        # Base Python dependencies
├── requirements_api.txt    # API dependencies (+FastAPI, Uvicorn, websockets)
├── .env.sample            # Environment template (minimal)
├── .env.example           # Environment template (full)
├── Dockerfile             # Container configuration
├── debates.jsonl          # Debate data storage (JSONL format)
│
├── api/                   # FastAPI/WebSocket modules
│   ├── __init__.py
│   ├── agents.py          # AutoGen agent creation (pro/con/judge)
│   ├── config.py          # Environment configuration
│   ├── debate.py          # Debate orchestration logic
│   ├── debate_view.py     # Debate view routes
│   ├── models.py          # Pydantic data models
│   ├── routes.py          # FastAPI route definitions
│   ├── speech.py          # TTS service implementation
│   └── websocket.py       # WebSocket connection manager
│
├── flask/                 # Flask REST API service
│   ├── app.py             # Flask app factory
│   ├── api.md             # API documentation
│   ├── debates.py         # Debate CRUD API
│   ├── debatefromnews.py  # News-to-debate generation
│   ├── photo.py           # Image generation API
│   ├── ttv.py             # SiliconFlow TTS
│   ├── ttv2.py            # Alternative TTS
│   ├── ttv3.py            # Huawei Cloud TTS
│   └── debates.jsonl      # Local copy of debate data
│
├── frontend/              # Vue.js frontend
│   ├── package.json       # Node dependencies
│   ├── vite.config.js     # Vite configuration
│   ├── index.html         # Entry HTML
│   └── src/
│       ├── main.js        # App entry
│       ├── App.vue        # Root component
│       ├── router/        # Vue Router config
│       ├── config/        # API config
│       ├── assets/        # Static assets
│       ├── components/    # Reusable components
│       └── views/         # Page components
│           ├── Login.vue
│           ├── HotDebates.vue
│           ├── DebateView.vue
│           ├── AddDebateTopic.vue
│           ├── Discover.vue
│           └── UserProfile.vue
│
├── model/                 # Model training (optional)
│   ├── train.py
│   ├── data.py
│   ├── test_app.py
│   └── customize_service.py
│
├── tests/                 # Test suite
│   ├── test_debate_api.py
│   ├── test_websocket.py
│   ├── test_llm.py
│   ├── test_speech.py
│   └── run_tests.py
│
├── audio_output/          # Generated audio files (Flask)
└── speech_output/         # Generated audio files (FastAPI)
```

## Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

**Required Variables:**
```env
# LLM Configuration (DeepSeek)
CUSTOM_LLM_API_KEY=sk-xxxxxxxx
CUSTOM_LLM_API_BASE=https://api.siliconflow.cn/v1
CUSTOM_LLM_MODEL=DeepSeek-V3

# Speech Configuration (SiliconFlow)
SPEECH_API_KEY=sk-xxxxxxxx
SPEECH_API_BASE=https://api.siliconflow.cn/v1
SPEECH_MODEL=FunAudioLLM/CosyVoice2-0.5B
SPEECH_VOICE=FunAudioLLM/CosyVoice2-0.5B:alex

# Server Settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8001
CORS_ORIGINS=["*"]
```

**Optional Variables:**
```env
# Speech Feature Flags
SPEECH_ENABLED=true
SPEECH_CACHE_ENABLED=true
SPEECH_SAMPLE_RATE=32000
SPEECH_CHUNK_SIZE=100

# Per-agent Voice Config
SUPPORTER_VOICE=alloy
OPPONENT_VOICE=echo
JUDGE_VOICE=onyx
SUPPORTER_SPEED=1.0
OPPONENT_SPEED=1.0
JUDGE_SPEED=1.0

# Debate Settings
DEFAULT_MAX_ROUNDS=10
```

## Build and Run Commands

### Development Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Install frontend dependencies
cd frontend && npm install
```

### Running Services

**CLI Mode (Direct Debate):**
```bash
python main.py
```

**FastAPI Server (WebSocket + REST):**
```bash
python server.py
# Runs on http://localhost:8001
```

**Flask API Server:**
```bash
cd flask && python app.py
# Runs on http://localhost:9000
```

**Frontend Dev Server:**
```bash
cd frontend && npm run dev
# Runs on http://localhost:3001
# Proxies /api to Flask server (port 5000)
```

### Production Build

```bash
cd frontend
npm run build
# Output: frontend/dist/
```

### Docker Deployment

```bash
# Build image
docker build -t ai-debate-system .

# Run container
docker run -p 8000:8000 \
  -e CUSTOM_LLM_API_KEY=xxx \
  -e CUSTOM_LLM_API_BASE=xxx \
  -e CUSTOM_LLM_MODEL=xxx \
  ai-debate-system
```

## Testing

### Run All Tests

```bash
# Ensure FastAPI server is running first
python server.py &

# Run tests
python tests/test_debate_api.py
```

### Individual Test Files

```bash
python tests/test_llm.py        # Test LLM connection
python tests/test_speech.py     # Test TTS service
python tests/test_websocket.py  # Test WebSocket
```

### Test Coverage

- `test_debate_api.py` - REST API endpoints (root, connection, debate, TTS)
- `test_websocket.py` - WebSocket streaming
- `test_llm.py` - LLM connectivity
- `test_speech.py` - Speech synthesis

## Code Style Guidelines

### Python

- **Encoding**: UTF-8, with `# -*- coding: utf-8 -*-` header
- **Docstrings**: Use triple-quoted docstrings for modules, classes, functions
- **Type Hints**: Use `typing` module for function signatures
- **Async**: Use `async/await` for I/O bound operations
- **Imports**: Group as: stdlib → third-party → local

Example:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module description
"""

import os
from typing import Dict, Any
from autogen import ConversableAgent

from api.config import LLM_CONFIG

def create_agent(name: str) -> ConversableAgent:
    """Create a debate agent."""
    pass
```

### Vue/JavaScript

- **Style**: Component files use Vue SFC format
- **API Calls**: Use Axios with async/await
- **Routing**: Use Vue Router with history mode

## Key API Endpoints

### FastAPI (Port 8001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/test_connection` | GET | Test LLM connection |
| `/debate` | POST | Start debate (sync) |
| `/text_to_speech` | POST | Convert text to speech |
| `/generate_speech_chunks` | POST | Chunked TTS |
| `/ws/debate` | WebSocket | Real-time debate streaming |

### Flask (Port 9000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/debates` | GET | List debates (paginated) |
| `/api/debate?debate_id=xxx` | GET | Get debate detail |
| `/api/addDebate` | POST | Create new debate |
| `/api/generate_debate` | POST | Generate from news URL |
| `/api/generate_speech` | POST | Generate speech |
| `/api/generate_photo?theme=xxx` | GET | Generate poster |
| `/audio_output/<filename>` | GET | Serve audio file |

## Data Storage

### debates.jsonl

Debates are stored in JSONL format (one JSON object per line):

```json
{
  "id": "uuid-string",
  "topic": "AI Pros vs Cons",
  "url": "https://source-url",
  "pros": {"team": "Team A", "argument": "Pro argument"},
  "cons": {"team": "Team B", "argument": "Con argument"},
  "poster": "https://image-url",
  "schedule": {"time": "2024-03-15 19:00", "location": "Online"},
  "status": "ongoing",
  "view_count": 235,
  "created_at": "2024-03-04T10:00:00",
  "rounds": [
    {"type": "emcee", "msg": "Intro text", "path": "audio_output/xxx.mp3"},
    {"type": "pro", "msg": "Pro argument", "path": "audio_output/xxx.mp3"},
    {"type": "con", "msg": "Con argument", "path": "audio_output/xxx.mp3"}
  ]
}
```

**Max Records**: 100 debates (configured in `flask/debates.py`)

## Security Considerations

1. **API Keys**: Never commit `.env` files. All keys are loaded from environment variables.

2. **CORS**: Flask/FastAPI allow all origins (`*`) by default. Restrict in production:
   ```python
   CORS_ORIGINS=["https://yourdomain.com"]
   ```

3. **Input Validation**: All API endpoints validate input parameters. Check `debates.py` for patterns.

4. **File Access**: Audio files are served from `audio_output/` with path sanitization.

5. **Rate Limiting**: Not implemented by default. Add Flask-Limiter for production.

## Common Development Tasks

### Adding a New API Endpoint

1. Define route in `flask/app.py` or `api/routes.py`
2. Add business logic in appropriate module
3. Update `flask/api.md` documentation
4. Add test in `tests/`

### Adding a New Agent Role

1. Edit `api/agents.py` → `create_agents()` or `create_judge_agent()`
2. Update system message template
3. Add voice config in `api/config.py` → `SPEECH_CONFIG`

### Modifying Frontend

1. Components go in `frontend/src/components/`
2. Pages go in `frontend/src/views/`
3. Add route in `frontend/src/router/index.js`
4. API base URL in `frontend/src/config/api.js`

## Troubleshooting

**LLM Connection Failed:**
- Check `.env` configuration
- Verify API key validity
- Test with `python tests/test_llm.py`

**Speech Generation Failed:**
- Verify SiliconFlow API key
- Check `SPEECH_ENABLED=true` in `.env`
- Check disk space in `speech_output/`

**WebSocket Not Connecting:**
- Ensure server.py is running on correct port
- Check firewall settings
- Verify CORS configuration

**Frontend API 404:**
- Check Vite proxy config in `vite.config.js`
- Verify Flask server is running
- Check port configuration

## References

- [README.md](./README.md) - User documentation (Chinese)
- [flask/api.md](./flask/api.md) - Detailed API documentation
- [docs/technical_architecture.md](./docs/technical_architecture.md) - Architecture overview
