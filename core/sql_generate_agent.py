from utils.file_utils import load_prompt
from utils.logger import pipeline_log

class SQLGenerateAgent:
    def __init__(self, model_name: str, prompt_path: str, llm_client):
        self.prompt = load_prompt(prompt_path)
        self.llm_client = llm_client
        self.model_name = model_name

    def __call__(self, inputs: dict) -> dict:
        preprocessed_json = inputs.get("preprocessed", "{}")

        try:
            # LLM Client 호출
            sql_query = self.llm_client.generate_response(
                system_prompt=self.prompt,
                user_message=preprocessed_json
            )

            # Markdown 코드 블록 제거 및 공백 정리
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            # 간단한 검증 (선택 사항)
            if not sql_query.lower().startswith("select") and not sql_query.lower().startswith("with"):
                pipeline_log("SQLGenerateAgent", "경고: SQL 형식이 아닌 응답일 수 있음")
                # 필요 시 여기서 sql_query = "" 처리

            pipeline_log("SQLGenerateAgent", f"SQL 생성: {sql_query}")

            return {"sql_query": sql_query, "input": inputs.get("input", "")}

        except Exception as e:
            pipeline_log("SQLGenerateAgent", f"오류: {e}")
            return {"sql_query": "", "input": inputs.get("input", "")}