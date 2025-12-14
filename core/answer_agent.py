from sqlalchemy import create_engine, text
from utils.file_utils import load_prompt
from utils.logger import pipeline_log

class AnswerAgent:
    def __init__(self, model_name: str, prompt_path: str, db_url: str, llm_client):
        """
        Args:
            model_name: 모델 이름 (로깅 또는 프롬프트 용도)
            prompt_path: 시스템 프롬프트 파일 경로
            db_url: 데이터베이스 연결 URL
            llm_client: LLMClient 인스턴스 (ClaudeLLMClient, GeminiLLMClient 등)
        """
        self.prompt = load_prompt(prompt_path)
        self.engine = create_engine(db_url)
        self.model_name = model_name
        self.llm_client = llm_client  # 외부에서 주입된 Client 저장

    def execute_sql(self, sql_query: str) -> list[dict]:
        """SQL 쿼리를 실행하고 결과를 딕셔너리 리스트로 반환"""
        if not sql_query:
            return []
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql_query))
                rows = [dict(zip(result.keys(), r)) for r in result.fetchall()]
            return rows
        except Exception as e:
            pipeline_log("AnswerAgent", f"SQL 실행 오류: {e}")
            return []

    def __call__(self, inputs: dict) -> dict:
        sql_query = inputs.get("sql_query", "")
        user_input = inputs.get("input", "")
        
        # 1. SQL 실행
        rows = self.execute_sql(sql_query)
        data_str = "\n".join(map(str, rows)) if rows else "[]"

        # 2. LLM 응답 생성
        try:
            # 사용자 메시지 구성 (질문 + 데이터)
            user_message = (
                f"[USER QUESTION]\n{user_input}\n\n"
                f"[SQL DATA]\n{data_str}"
            )

            # 주입받은 llm_client를 사용하여 응답 생성
            # 주의: LLMClient 클래스들(Claude, Gemini 등)은 
            # generate_response(system_prompt, user_message) 메서드를 공통적으로 구현해야 합니다.
            final_answer = self.llm_client.generate_response(
                system_prompt=self.prompt,
                user_message=user_message
            )
            
            pipeline_log("AnswerAgent", f"요약: {final_answer}")

        except Exception as e:
            final_answer = "데이터 요약 중 오류 발생"
            pipeline_log("AnswerAgent", f"요약 오류: {e}")

        pipeline_log("END", "=" * 80)

        return {"final_answer": final_answer}