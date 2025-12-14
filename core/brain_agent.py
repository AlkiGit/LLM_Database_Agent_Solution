from utils.file_utils import load_prompt
from utils.logger import pipeline_log
import json

class BrainAgent:
    def __init__(self, model_name: str, prompt_path: str, llm_client):
        self.prompt = load_prompt(prompt_path)
        self.llm_client = llm_client
        self.model_name = model_name
        
    def __call__(self, inputs: dict) -> dict:
        user_input = inputs.get("input", "")
        pipeline_log("INPUT", user_input)

        # 사용자 입력 구성
        content_text = f"[USER_INPUT]\n{user_input}"

        try:
            # LLM Client 호출
            raw = self.llm_client.generate_response(
                system_prompt=self.prompt,
                user_message=content_text
            )
            
            # Markdown 코드 블록(```json ... ```) 제거 등 문자열 정리
            cleaned_raw = raw.replace("```json", "").replace("```", "").strip()
            
            # JSON 파싱
            out = json.loads(cleaned_raw)
            
            pipeline_log("BrainAgent", f"결과: {json.dumps(out, ensure_ascii=False)}")
            return {"brain_decision": out, "input": user_input}

        except json.JSONDecodeError as json_e:
            pipeline_log("BrainAgent", f"오류: JSON 디코딩 실패. 원본: {raw}")
            # JSON 파싱 실패 시 에러 상태 반환
            return {
                "brain_decision": {"action": "ERROR", "query": user_input, "reasoning": f"JSON Decode Error: {json_e}"},
                "input": user_input
            }
        except Exception as e:
            pipeline_log("BrainAgent", f"오류: {e}")
            return {
                "brain_decision": {"action": "ERROR", "query": user_input, "reasoning": str(e)},
                "input": user_input
            }