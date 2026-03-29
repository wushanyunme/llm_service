from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.core.orchestrator import Orchestrator 
from app.core.router import ModelRouter
from app.adapters.openai_adapter import OpenAIAdapter

router = APIRouter()

open_adapter = OpenAIAdapter(
    api_key="your_openai_api_key",
    base_url="https://api.openai.com/v1",
    model="gpt-4o-mini"
)

deepseek_adapter = OpenAIAdapter(
    api_key="your_deepseek_api_key",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat"
)

router_model = ModelRouter({
    "openai": open_adapter,
    "deepseek": deepseek_adapter
})

orch = Orchestrator(router_model)

@router.post("/chat")
def chat(req: ChatRequest):
    return {"response" : orch.chat(req)}

@router.post("/chat/stream")
def chat_stream(req: ChatRequest):
    return StreamingResponse(orch.stream(req), media_type="text/plain")  