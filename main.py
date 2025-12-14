from graph_builder import build_graph
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    graph = build_graph()

    print("LangGraph 기반 재무 데이터 어시스턴트 실행 중. 종료하려면 exit 입력.\n")

    while True:
        q = input("질문: ")
        if q.lower() in ["exit", "quit"]:
            break
        result = graph.invoke({"input": q})
        print("\n[응답]:", result.get("final_answer", "결과 없음"))
        print("=" * 60)
