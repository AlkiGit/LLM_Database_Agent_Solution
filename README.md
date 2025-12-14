프로젝트의 구조(LangGraph, Multi-LLM, SQLAlchemy 등)를 완벽하게 반영한 전문적인 README.md 초안입니다.

이 파일을 프로젝트 최상위 경로에 저장하시면, GitHub이나 GitLab에 올렸을 때 프로젝트의 정체성을 명확하게 보여줄 수 있습니다.

🤖 AI Database Analyst (Text-to-SQL Agent)
LangGraph 기반의 에이전트 파이프라인을 통해 자연어 질문을 SQL로 변환하고, 데이터베이스에서 조회한 결과를 분석하여 답변을 제공하는 AI 시스템입니다.

✨ 주요 기능 (Key Features)
Multi-LLM Support: Google Gemini, Anthropic Claude, OpenAI GPT 모델 중 원하는 모델을 선택하여 사용할 수 있는 유연한 구조 (Dependency Injection 적용).

LangGraph Pipeline: 명확한 상태 관리와 에이전트 간의 흐름 제어.

Modular Agent System: 각 역할에 특화된 에이전트 구성.

🧠 Brain Agent: 사용자 의도 파악 및 라우팅.

🧹 Preprocessing Agent: 질문 정제 및 명확화.

💻 SQL Generate Agent: 데이터베이스 스키마 기반 SQL 쿼리 생성.

📊 Answer Agent: SQL 실행 및 결과 데이터를 기반으로 최종 답변 요약.

SQLAlchemy Integration: 다양한 데이터베이스(PostgreSQL, MySQL 등)와의 호환성 확보.

🏗️ 아키텍처 (Architecture)
이 프로젝트는 LangGraph를 사용하여 다음과 같은 순차적 흐름(StateGraph)을 따릅니다.

코드 스니펫

graph LR
    Start([User Input]) --> Brain[🧠 Brain Agent]
    Brain --> Pre[🧹 Preprocessing Agent]
    Pre --> SQL[💻 SQL Generate Agent]
    SQL --> Answer[📊 Answer Agent]
    Answer --> End([Final Answer])
Brain Agent: 사용자의 질문을 분석하여 필요한 정보가 무엇인지 판단합니다.

Preprocessing Agent: 모호한 질문을 구체화하거나 불필요한 정보를 제거합니다.

SQL Generate Agent: 정제된 질문을 실행 가능한 SQL 쿼리로 변환합니다.

Answer Agent: 생성된 SQL을 DB에서 실행하고, 조회된 데이터를 자연어로 요약하여 사용자에게 전달합니다.

🛠️ 설치 및 설정 (Installation)
1. 프로젝트 클론
Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. 가상환경 생성 및 활성화
Bash

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
3. 패키지 설치
Bash

pip install -r requirements.txt
4. 환경 변수 설정 (.env)
프로젝트 루트에 .env 파일을 생성하고 아래 내용을 본인의 환경에 맞게 입력하세요.

Ini, TOML

# Database Connection (SQLAlchemy 형식)
# 예: postgresql://user:password@localhost:5432/mydatabase
DATABASE_URL=your_database_url_here

# LLM API Keys (사용할 모델의 키만 입력해도 됩니다)
GOOGLE_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
🚀 사용 방법 (Usage)
LLM 모델 변경 방법
graph_builder.py 파일 내에서 사용할 LLM 클라이언트를 선택할 수 있습니다.

Python

# graph_builder.py

def build_graph():
    # ...
    
    # 사용할 모델의 주석을 해제하세요
    # 1. Google Gemini
    llm_client = GeminiLLMClient(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # 2. Anthropic Claude
    # llm_client = ClaudeLLMClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # ...
실행
메인 애플리케이션을 실행하여 에이전트와 대화합니다.

Bash

python main.py
(참고: 진입점 파일명이 main.py가 아니라면 해당 파일명으로 실행하세요)

📂 프로젝트 구조 (Project Structure)
.
├── agents/                 # 각 에이전트의 프롬프트 파일 (.txt)
│   ├── brain_agent.txt
│   ├── answer_agent.txt
│   └── ...
├── core/                   # 에이전트 로직 구현 (Python Classes)
│   ├── brain_agent.py
│   ├── sql_generate_agent.py
│   ├── answer_agent.py     # DI 패턴이 적용된 답변 에이전트
│   └── llm_clients/        # LLM별 클라이언트 구현체 (Claude, Gemini, OpenAI)
├── utils/                  # 유틸리티 (로거, 파일 로더 등)
├── graph_builder.py        # LangGraph 구성 및 조립
├── main.py                 # 실행 진입점
├── requirements.txt        # 의존성 패키지 목록
└── .env                    # 환경 변수 (Git 제외)

📦 기술 스택 (Tech Stack)
Language: Python 3.9+

Orchestration: LangGraph, LangChain

LLMs: Google Gemini (via google-genai), Anthropic Claude, OpenAI GPT

Database: SQLAlchemy

Configuration: Python-dotenv

📝 License
This project is licensed under the MIT License.