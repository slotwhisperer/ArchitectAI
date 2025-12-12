# config.py — ARCHITECT AI (2025)
# Monero Only • No Refunds • No Leaks

import os
from dotenv import load_dotenv

load_dotenv()

# Groq 70B (free tier works without key for low traffic)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Optional: RunPod / Vast.ai (for your future 70B+ cloud)
RUNPOD_ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

# Optional: Telegram bot for client intake
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Optional: Monero wallet (auto-payment checker)
MONERO_ADDRESS = os.getenv("MONERO_ADDRESS")
MONERO_VIEW_KEY = os.getenv("MONERO_VIEW_KEY")  # for read-only balance check

# Optional: Streamlit sharing
STREAMLIT_SHARING = os.getenv("STREAMLIT_SHARING", "public")

# Optional: Local Ollama (if you ever run locally again)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
