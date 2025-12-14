# utils/file_utils.py
import os

def load_prompt(path: str) -> str:
    """에이전트용 프롬프트 파일을 읽어 반환"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt 파일을 찾을 수 없습니다: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
