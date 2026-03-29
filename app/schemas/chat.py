from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    session_id: str
    prompt: str
    model: Optional[str] = "auto"
    stream: Optional[bool] = False