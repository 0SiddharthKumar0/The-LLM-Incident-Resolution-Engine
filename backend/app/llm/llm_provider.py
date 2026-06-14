import requests

from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=env_path)

OLLAMA_URL = os.getenv("OLLAMA_URL")


def generate_response(prompt: str):

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    return response.json()["response"]