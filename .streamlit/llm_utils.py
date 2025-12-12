# llm_utils.py — ARCHITECT AI (2025)
# Monero Only • No Refunds • No External APIs Banned

import requests
from urllib.parse import urljoin
from langchain_ollama import ChatOllama
from typing import List, Optional
from langchain_core.callbacks.base import BaseCallbackHandler

class BufferedStreamingHandler(BaseCallbackHandler):
    """Smooth token streaming for your elite UI"""
    def __init__(self, ui_callback=None):
        self.buffer = ""
        self.ui_callback = ui_callback

    def on_llm_new_token(self, token: str, **kwargs):
        self.buffer += token
        if "\n" in token or len(self.buffer) >= 60:
            if self.ui_callback:
                self.ui_callback(self.buffer)
            self.buffer = ""

    def on_llm_end(self, response, **kwargs):
        if self.buffer and self.ui_callback:
            self.ui_callback(self.buffer)
        self.buffer = ""

# Only one callback — elite streaming
streaming_handler = BufferedStreamingHandler()

# Only one model allowed — your custom ARCHITECT
_llm_config = {
    "class": ChatOllama,
    "constructor_params": {
        "model": "architect",
        "base_url": "http://localhost:11434",
        "temperature": 0.3,
        "streaming": True,
        "callbacks": [streaming_handler]
    }
}

def get_model_choices() -> List[str]:
    """Only one choice — perfection"""
    return ["architect"]

def resolve_model_config(model_choice: str):
    """Always returns your ARCHITECT model"""
    if "architect" in model_choice.lower():
        return _llm_config
    return None

def fetch_ollama_models() -> List[str]:
    """Just checks if your model exists"""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            models = r.json().get("models", [])
            return [m.get("name") or m.get("model") for m in models]
    except:
        pass
    return []
