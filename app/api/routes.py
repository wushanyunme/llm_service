from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.core.orchestrator import Orchestrator 
from app.core.router import ModelRouter
from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.gemini_adapter import GeminiAdapter

from dotenv import load_dotenv  # 导入
import os

load_dotenv()

router = APIRouter()

# 初始化适配器字典
adapters = {}

# 初始化 OpenAI 适配器
try:
    if os.getenv("OPENAI_API_KEY"):
        adapters["openai"] = OpenAIAdapter(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
            model="gpt-4o-mini"
        )
except Exception as e:
    print(f"Warning: OpenAI adapter initialization failed: {e}")

# 初始化 DeepSeek 适配器
try:
    if os.getenv("DEEPSEEK_API_KEY"):
        adapters["deepseek"] = OpenAIAdapter(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat"
        )
except Exception as e:
    print(f"Warning: DeepSeek adapter initialization failed: {e}")

# 初始化 Gemini 适配器
try:
    if os.getenv("GEMINI_API_KEY"):
        adapters["gemini"] = GeminiAdapter(
            api_key=os.getenv("GEMINI_API_KEY"),
            model="models/gemini-2.5-flash"
        )
except Exception as e:
    print(f"Warning: Gemini adapter initialization failed: {e}")

# 确保至少有一个适配器
if not adapters:
    raise RuntimeError("No LLM adapters configured. Please set at least one API key in .env file")

router_model = ModelRouter(adapters)

orch = Orchestrator(router_model)

@router.post("/chat")
def chat(req: ChatRequest):
    return {"response" : orch.chat(req)}

@router.post("/chat/stream")
def chat_stream(req: ChatRequest):
    return StreamingResponse(orch.stream(req), media_type="text/plain")  