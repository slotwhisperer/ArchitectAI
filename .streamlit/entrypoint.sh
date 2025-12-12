#!/usr/bin/env bash
# entrypoint.sh — ARCHITECT AI (2025)
# Monero Only • No Refunds • No Mercy

set -e  # Exit on any error

echo "============================================"
echo "     ARCHITECT AI — Starting Secure Node"
echo "     Monero Only • Escrow First • 2025"
echo "============================================"

# Optional: Wait for Ollama if running locally (most people use cloud now)
if [[ -n "$OLLAMA_BASE_URL" ]]; then
    echo "Waiting for Ollama at $OLLAMA_BASE_URL..."
    until curl -s "$OLLAMA_BASE_URL/api/tags" > /dev/null; do
        echo "Ollama not ready, retrying in 3s..."
        sleep 3
    done
    echo "Ollama connected"
fi

# Optional: Wait for Groq/RunPod health
if [[ -n "$GROQ_API_KEY" ]] || [[ -n "$RUNPOD_ENDPOINT_ID" ]]; then
    echo "Cloud LLM ready (Groq/RunPod)"
fi

echo "Launching ARCHITECT AI interface..."
echo "Access: http://localhost:8501"

# Run the empire
exec streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
