from utils.file_utils import load_prompt
from utils.logger import pipeline_log

class PreprocessingAgent:
    def __init__(self, model_name: str, prompt_path: str, llm_client):
        """
        Args:
            llm_client: LLMClient 인스턴스 (generate_response 메서드를 가져야 함)
        """
        self.prompt = load_prompt(prompt_path)
        self.llm_client = llm_client  # 주입된 클라이언트 저장
        self.model_name = model_name

    def __call__(self, inputs: dict) -> dict:
        user_input = inputs.get("input", "")
        
        try:
            # LLM Client를 통해 응답 생성
            result = self.llm_client.generate_response(
                system_prompt=self.prompt,
                user_message=user_input
            )

            pipeline_log("PreprocessingAgent", f"결과: {result}")
            return {"preprocessed": result, "input": user_input}

        except Exception as e:
            pipeline_log("PreprocessingAgent", f"오류: {e}")
            # 오류 발생 시 빈 JSON 객체 문자열 반환
            return {"preprocessed": "{}", "input": user_input}