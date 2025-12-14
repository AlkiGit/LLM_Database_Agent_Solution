import os
from google import genai
from google.genai import types

class GeminiLLMClient:
    def __init__(self, model_name: str, api_key: str = None):
        """
        Gemini 클라이언트 초기화
        """
        self.model_name = model_name
        
        # 1. 인자로 받은 api_key가 있으면 사용
        # 2. 없으면 환경변수 'GEMINI_API_KEY' 확인 (사용자 설정)
        # 3. 그것도 없으면 'GOOGLE_API_KEY' 확인 (SDK 기본값)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("API Key가 설정되지 않았습니다. .env 파일에 GEMINI_API_KEY를 설정해주세요.")

        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, system_prompt: str, user_message: str, temperature: float = 0.0) -> str:
        # ... (이전 코드와 동일) ...
        config = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_prompt
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    {"role": "user", "parts": [{"text": user_message}]}
                ],
                config=config
            )
            if response.text:
                return response.text.strip()
            return ""

        except Exception as e:
            print(f"[GeminiLLMClient] Error: {e}")
            raise e