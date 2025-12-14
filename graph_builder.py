from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
from dotenv import load_dotenv

# Agents
from core.brain_agent import BrainAgent
from core.preprocessing_agent import PreprocessingAgent
from core.sql_generate_agent import SQLGenerateAgent
from core.answer_agent import AnswerAgent

# LLM Clients (3가지 모두 임포트)
from agents.llm_clients.gemini_client import GeminiLLMClient
from agents.llm_clients.openai_client import OpenAILLMClient
from agents.llm_clients.claude_client import ClaudeLLMClient

# .env 로드
load_dotenv()

class AgentState(TypedDict, total=False):
    input: str
    brain_decision: dict
    preprocessed: str
    sql_query: str
    final_answer: str

def build_graph():
    # 데이터베이스 URL
    db_url = os.getenv("DATABASE_URL")
    
    # ============================================================
    # 1. 사용할 LLM 모델 선택 (여기만 주석을 해제/설정하면 됨)
    # ============================================================
    
    # [옵션 A] Gemini (현재 설정)
    provider = "google"
    model_name = "gemini-2.5-flash"

    # [옵션 B] OpenAI (GPT-4o)
    # provider = "openai"
    # model_name = "gpt-4o"

    # [옵션 C] Anthropic (Claude 3.5 Sonnet)
    # provider = "anthropic" 
    # model_name = "claude-3-7-sonnet-20250219" 


    # ============================================================
    # 2. 선택된 Provider에 따라 Client 생성
    # ============================================================
    llm_client = None

    if provider == "google":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: raise ValueError("GEMINI_API_KEY가 없습니다.")
        llm_client = GeminiLLMClient(model_name=model_name, api_key=api_key)
        
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key: raise ValueError("OPENAI_API_KEY가 없습니다.")
        llm_client = OpenAILLMClient(model_name=model_name, api_key=api_key)
        
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key: raise ValueError("ANTHROPIC_API_KEY가 없습니다.")
        llm_client = ClaudeLLMClient(model_name=model_name, api_key=api_key)
    
    else:
        raise ValueError(f"지원하지 않는 Provider입니다: {provider}")

    print(f"✅ 현재 사용 중인 LLM Provider: {provider} / Model: {model_name}")


    # ============================================================
    # 3. 에이전트 초기화 (Dependency Injection)
    # ============================================================
    # 어떤 Client가 들어오든 generate_response 메서드가 있으므로 동일하게 작동함
    
    brain = BrainAgent(
        model_name=model_name,
        prompt_path="agents/brain_agent.txt",
        llm_client=llm_client 
    )

    pre = PreprocessingAgent(
        model_name=model_name,
        prompt_path="agents/preprocessing_agent.txt",
        llm_client=llm_client
    )

    sqlgen = SQLGenerateAgent(
        model_name=model_name,
        prompt_path="agents/sql_generate_agent.txt",
        llm_client=llm_client
    )

    answer = AnswerAgent(
        model_name=model_name,
        prompt_path="agents/answer_agent.txt",
        db_url=db_url,
        llm_client=llm_client
    )

    # ============================================================
    # 4. LangGraph 구성 (변경 없음)
    # ============================================================

    graph = StateGraph(AgentState)

    graph.add_node("brain", brain)
    graph.add_node("pre", pre)
    graph.add_node("sqlgen", sqlgen)
    graph.add_node("answer", answer)

    graph.add_edge("brain", "pre")
    graph.add_edge("pre", "sqlgen")
    graph.add_edge("sqlgen", "answer")
    graph.add_edge("answer", END)

    graph.set_entry_point("brain")

    return graph.compile()