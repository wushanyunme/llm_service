import pytest
from app.adapters.gemini_adapter import GeminiAdapter

from dotenv import load_dotenv  # 导入
import os

load_dotenv()

@pytest.fixture
def gemini_adapter():
    
    return GeminiAdapter(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="models/gemini-2.5-flash"
    )

def test_gemini_chat(gemini_adapter):
    test_messages = [
        {"role": "user", "content": "Hello, Gemini!"},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]
    
    response = gemini_adapter.chat(test_messages)
    
    assert isinstance(response, str), "Gemini response should be a string"
    assert len(response) > 0, "Gemini response should not be empty"


