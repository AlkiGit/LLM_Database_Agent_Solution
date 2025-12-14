import os
import time
from openai import OpenAI, RateLimitError

class OpenAILLMClient:
    def __init__(self, model_name: str, api_key: str = None):
        """
        OpenAI 클라이언트 초기화
        """
        self.model_name = model_name
        # 인자로 받은 키가 없으면 환경변수 확인
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API Key가 설정되지 않았습니다.")

        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, system_prompt: str, user_message: str, temperature: float = 0.0) -> str:
        """
        OpenAI Chat Completion API 호출
        """
        max_retries = 3
        base_delay = 2

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()

            except RateLimitError:
                # 429 에러 처리
                wait_time = base_delay * (2 ** attempt)
                print(f"[OpenAILLMClient] Rate Limit Exceeded. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            
            except Exception as e:
                print(f"[OpenAILLMClient] Error: {e}")
                raise e
        
        raise Exception("OpenAI API Max retries exceeded.")