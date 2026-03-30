# Gemini API 集成使用指南

## 功能说明

本项目已成功集成 Google Gemini 大模型 API，支持以下功能：
- 标准聊天接口
- 流式响应

## 配置步骤

### 1. 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 点击 "Create API Key" 生成新的 API 密钥
3. 复制 API Key

### 2. 配置环境变量

在项目根目录的 `.evn` 文件中添加：

```
GEMINI_API_KEY=your_gemini_api_key_here
```

将 `your_gemini_api_key_here` 替换为你的实际 API Key。

## API 使用说明

### 标准聊天请求

**请求地址:** `POST /api/v1/chat`

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "prompt": "你好，请介绍一下自己",
    "model": "gemini",
    "stream": false
  }'
```

**Response:**
```json
{
  "response": "你好！我是 Claude，由 Anthropic 开发的 AI 助手..."
}
```

### 流式聊天请求

**请求地址:** `POST /api/v1/chat/stream`

**请求示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "prompt": "请写一首关于春天的诗",
    "model": "gemini",
    "stream": true
  }'
```

## 支持的模型选项

- `"gemini"` - 自动选择 Gemini 1.5 Flash（推荐）
- `"openai"` - OpenAI GPT-4o mini
- `"deepseek"` - DeepSeek Chat
- `"auto"` - 自动选择（基于提示词内容）

## 参数说明

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `session_id` | string | 会话ID，用于维护对话历史 | "user_123_session" |
| `prompt` | string | 用户提示词 | "告诉我关于..." |
| `model` | string | 模型选择（可选，默认为 "auto"） | "gemini" |
| `stream` | boolean | 是否使用流式响应（可选，默认为 false） | true |

## 项目文件结构

```
app/
├── adapters/
│   ├── openai_adapter.py      # OpenAI 适配器
│   ├── deepseek_adapter.py    # DeepSeek 适配器
│   └── gemini_adapter.py      # Gemini 适配器 (新增)
├── api/
│   └── routes.py              # API 路由（已更新）
├── core/
│   ├── orchestrator.py        # 请求协调器
│   ├── router.py              # 模型路由器
│   └── memory.py              # 会话记忆管理
└── schemas/
    └── chat.py                # 数据模型

.env                           # 环境变量 (包含 GEMINI_API_KEY)
dev-requirements.txt           # 依赖包（已更新）
```

## 技术特点

- ✅ 适配器模式，易于添加新模型
- ✅ 支持会话历史管理
- ✅ 支持流式响应
- ✅ 统一的 API 接口
- ✅ 完全支持 Gemini 最新特性

## 故障排除

### 问题：API Key 无效
**解决方案：** 检查 `.evn` 文件中 `GEMINI_API_KEY` 是否正确配置

### 问题：模型不可用
**解决方案：** 确保你的 Gemini 账户有足够配额，访问 [Google AI Studio](https://aistudio.google.com/app/apikey) 检查状态

### 问题：超时或连接失败
**解决方案：** 检查网络连接，确保可以访问 Google API

## 更新日志

### v1.1.0 - Gemini 支持
- [x] 创建 GeminiAdapter 类
- [x] 支持标准聊天接口
- [x] 支持流式响应
- [x] 集成到 ModelRouter
- [x] 更新环境配置
- [x] 更新依赖列表
