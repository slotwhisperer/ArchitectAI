from langchain_core.callbacks import BaseCallbackHandler

class BufferedStreamingHandler(BaseCallbackHandler):
    """Stream output into a buffer."""
    def __init__(self, buffer):
        self.buffer = buffer

    def on_llm_new_token(self, token, **kwargs):
        self.buffer += token

def get_model_choices():
    """Only allow local Ollama models."""
    return ["architect"]
