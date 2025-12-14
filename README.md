# 🤖 AI Database Analyst (Text-to-SQL Agent)

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-FF4B4B)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **LangGraph** 기반의 에이전트 파이프라인을 통해 자연어 질문을 SQL로 변환하고, 데이터베이스에서 조회한 결과를 분석하여 답변을 제공하는 시스템입니다.

<br>

  * Google Gemini, Anthropic Claude, OpenAI GPT 중 원하는 모델을 선택하여 사용할 수 있습니다.
  * 각 역할에 특화된 전문 에이전트들이 협업하는 구조입니다.
  * Brain, Preprocessing, SQL Generator, Answer Agent로 구성됩니다.

<br>

## 🏗️ Architecture

```mermaid
graph LR
    User([👤 User Input]) --> Brain[🧠 Brain Agent]
    Brain --> Pre[🧹 Preprocessing]
    Pre --> SQL[💻 SQL Generate]
    SQL --> Answer[📊 Answer Agent]
    
    subgraph "Database Layer"
        SQL -.->|Execute Query| DB[(🗄️ Database)]
        DB -.->|Return Rows| Answer
    end
    
    Answer --> End([🏁 Final Answer])
    
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style DB fill:#bbf,stroke:#333,stroke-width:2px
```

<br>

### 🤖 에이전트 역할 (Agents)

| 에이전트 이름 | 역할 설명 |
| :--- | :--- |
| **🧠 Brain Agent** | 사용자의 질문을 분석하여 의도를 파악하고, 전체적인 워크플로우를 조율합니다. |
| **🧹 Preprocessing Agent** | 모호한 자연어 질문을 구체화하거나, 분석에 방해되는 불필요한 정보를 제거합니다. |
| **💻 SQL Generate Agent** | 정제된 질문과 데이터베이스 스키마를 바탕으로 실행 가능한 SQL 쿼리를 생성합니다. |
| **📊 Answer Agent** | 생성된 SQL을 DB에서 실행하고, 조회된 결과 데이터를 종합하여 자연어로 답변합니다. |

<br>

## 🛠️ 설치 및 설정 (Installation)

### 1. 프로젝트 클론
```bash
git clone [https://github.com/AlkiGit/DB_Agent_Multimodel.git](https://github.com/AlkiGit/DB_Agent_Multimodel.git)
cd DB_Agent_Multimodel
```

### 2. 가상환경 생성 및 활성화
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정 (.env)
프로젝트 루트 경로에 `.env` 파일을 생성하고 아래 내용을 본인의 환경에 맞게 수정하세요.

```ini
# Database Connection (SQLAlchemy URL 형식)
# 예: postgresql://user:password@localhost:5432/mydatabase
DATABASE_URL=your_database_url_here

# LLM API Keys (사용할 모델의 키만 입력하면 됩니다)
GOOGLE_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
```

<br>

## 🚀 사용 방법 (Usage)

### 1️⃣ LLM 모델 선택
`graph_builder.py` 파일 내에서 주석을 해제하여 사용할 LLM 클라이언트를 선택할 수 있습니다.

```python
# graph_builder.py

def build_graph():
    # ...
    
    # [옵션] 사용할 모델의 주석을 해제하세요
    
    # 1. Google Gemini (Default)
    llm_client = GeminiLLMClient(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # 2. Anthropic Claude
    # llm_client = ClaudeLLMClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # ...
```

### 2️⃣ 실행
메인 애플리케이션을 실행하여 에이전트와 대화를 시작합니다.

```bash
python main.py
```

<br>

## 📂 프로젝트 구조 (Project Structure)

```bash
📦 DB_Agent_Multimodel
 ┣ 📂 agents/                # 시스템 프롬프트 관리 (.txt)
 ┃ ┣ 📂 llm_clients/         # 벤더별 LLM 클라이언트 (Gemini, Claude, GPT)
 ┃ ┣ 📜 brain_agent.txt
 ┃ ┣ 📜 answer_agent.txt
 ┃ ┗ ...
 ┣ 📂 core/                  # 에이전트 및 LLM 로직 구현
 ┃ ┣ 📜 brain_agent.py
 ┃ ┣ 📜 answer_agent.py
 ┃ ┗ ...
 ┣ 📂 utils/                 # 유틸리티 (로거, 파일 로더)
 ┣ 📜 graph_builder.py       # LangGraph 파이프라인 조립
 ┣ 📜 main.py                # 실행 진입점
 ┣ 📜 requirements.txt       # 의존성 패키지
 ┗ 📜 .env                   # 환경 변수 (Git 제외)
```

<br>

## 📦 기술 스택 (Tech Stack)

* **Language:** Python 3.9+
* **Orchestration:** LangGraph, LangChain
* **LLMs:**
  * Google Gemini (`google-genai`)
  * Anthropic Claude
  * OpenAI GPT
* **Database:** SQLAlchemy (PostgreSQL, MySQL, SQLite supported)
* **Configuration:** Python-dotenv

<br>

## 📝 License

README Written with Gemini-3.0-pro


This project is licensed under the MIT License.