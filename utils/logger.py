# utils/logger.py
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/results.json")
PIPELINE_LOG = Path("logs/pipeline.log")

def timestamp() -> str:
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def save_json_log(entry: dict):
    """최종 결과를 JSON으로 저장 (기존)"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if LOG_FILE.exists():
        try:
            data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = []
    else:
        data = []
    data.append(entry)
    LOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def pipeline_log(stage: str, message: str):
    """단계별 로그를 텍스트로 기록"""
    PIPELINE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PIPELINE_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp()} [{stage}] {message}\n")
