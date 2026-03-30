from google import genai
from typing import List


class GeminiAdapter:
    """Google Gemini API 适配器"""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        初始化 Gemini 适配器
        
        Args:
            api_key: Google Gemini API key
            model: 使用的模型，默认为 gemini-2.5-flash
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment variables")
        
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def chat(self, messages: List[dict]) -> str:
        """
        发送聊天请求到 Gemini
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}, ...]
        
        Returns:
            Gemini 的回复文本
        """
        try:
            # 将消息转换为 google.genai 支持的格式
            formatted_messages = []
            last_user_message = None
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                # 转换角色名称
                if role == "assistant":
                    formatted_role = "model"
                else:
                    formatted_role = role
                    last_user_message = content  # 跟踪最后一条用户消息
                    
                formatted_messages.append({
                    "role": formatted_role,
                    "parts": [{"text": content}]
                })
            
            # 如果最后一条消息不是用户消息，需要添加一个新的用户消息来触发回复
            if formatted_messages and formatted_messages[-1]["role"] != "user":
                if last_user_message is None:
                    last_user_message = "Continue the conversation."
                formatted_messages.append({
                    "role": "user",
                    "parts": [{"text": last_user_message}]
                })
            
            # 使用新 API 调用方式
            response = self.client.models.generate_content_stream(
                model=self.model,  # 模型名称已包含 models/ 前缀
                contents=formatted_messages
            )
            
            # 收集流式响应
            result_text = ""
            for chunk in response:
                if chunk.text:
                    result_text += chunk.text
            
            return result_text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    def stream(self, messages: List[dict]):
        """
        发送流式聊天请求到 Gemini
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}, ...]
        
        Yields:
            Gemini 的流式回复内容
        """
        try:
            # 将消息转换为 google.genai 支持的格式
            formatted_messages = []
            last_user_message = None
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                # 转换角色名称
                if role == "assistant":
                    formatted_role = "model"
                else:
                    formatted_role = role
                    last_user_message = content  # 跟踪最后一条用户消息
                    
                formatted_messages.append({
                    "role": formatted_role,
                    "parts": [{"text": content}]
                })
            
            # 如果最后一条消息不是用户消息，需要添加一个新的用户消息来触发回复
            if formatted_messages and formatted_messages[-1]["role"] != "user":
                if last_user_message is None:
                    last_user_message = "Continue the conversation."
                formatted_messages.append({
                    "role": "user",
                    "parts": [{"text": last_user_message}]
                })
            
            # 发送流式请求（使用新 API）
            response = self.client.models.generate_content_stream(
                model=self.model,  # 模型名称已包含 models/ 前缀
                contents=formatted_messages
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
