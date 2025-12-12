# llm_utils.py — ARCHITECT AI Edition (2025)
# Designed for exclusive use with your custom Ollama model: architect

import requests
from urllib.parse import urljoin
from langchain_ollama import ChatOllama
from typing import Callable, Optional, List
from langchain_core.callbacks.base import BaseCallbackHandler

class BufferedStreamingHandler(BaseCallbackHandler):
    """Streams tokens to UI with buffering for smooth display"""
    def __init__(self, buffer_limit: int = 60, ui_callback: Optional[Callable[[str], None]] = None):
        self.buffer = ""
        self.buffer_limit = buffer_limit
        self.ui_callback = ui_callback

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.buffer += token
        if "\n" in token or len(self.buffer) >= self.buffer_limit:
            if self.ui_callback:
                self.ui_callback(self.buffer)
            self.buffer = ""

    def on_llm_end(self, response, **kwargs) -> None:
        if self.buffer and self.ui_callback:
            self.ui_callback(self.buffer)
        self.buffer = ""

# Common streaming handler
_common_callbacks = [BufferedStreamingHandler(buffer_limit=60)]

# Common parameters for all LLMs
_common_llm_params = {
    "temperature": 0.3,
    "streaming": True,
    "callbacks": _common_callbacks,
}

# Only one model: your custom ARCHITECT AI
_llm_config_map = {
    "architect": {
        "class": ChatOllama,
        "constructor_params": {
            "model": "architect",
            "base_url": "http://localhost:11434"  # Standard Ollama port
        }
    }
}

def _normalize_model_name(name: str) -> str:
    return name.strip().lower()

def fetch_ollama_models() -> List[str]:
    """Check if Ollama is running and get available models"""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=3)
        resp.raise_for_status()
        models = resp.json().get("models", [])
        return [m.get("name") or m.get("model") for m in models if m.get("name") or m.get("model")]
    except:
        return []

def get_model_choices() -> List[str]:
    """Return only your ARCHITECT model (keeps UI clean)"""
    available = fetch_ollama_models()
 Maggiore    if "architect" in [m.lower() for m in available]:
        return ["architect"]
    return ["architect"]  # Force it — it's your only model

def resolve_model_config(model_choice: str):
    """Resolve to your ARCHITECT model"""
    if _normalize_model_name(model_choice) == "architect":
        return _llm_config_map["architect"]
    return None
