import os
import time
import anthropic

class ClaudeLLMClient:
    def __init__(self, model_name: str, api_key: str = None):
        """
        Anthropic Claude 클라이언트 초기화
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("Anthropic API Key가 설정되지 않았습니다.")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_response(self, system_prompt: str, user_message: str, temperature: float = 0.0) -> str:
        """
        Anthropic Messages API 호출
        """
        max_retries = 3
        base_delay = 2

        for attempt in range(max_retries):
            try:
                message = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=4096,  # Claude는 max_tokens 필수
                    temperature=temperature,
                    system=system_prompt,  # Claude는 system 파라미터가 별도로 존재
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                return message.content[0].text.strip()

            except anthropic.RateLimitError:
                wait_time = base_delay * (2 ** attempt)
                print(f"[ClaudeLLMClient] Rate Limit Exceeded. Retrying in {wait_time}s...")
                time.sleep(wait_time)

            except Exception as e:
                print(f"[ClaudeLLMClient] Error: {e}")
                raise e
                
        raise Exception("Anthropic API Max retries exceeded.")