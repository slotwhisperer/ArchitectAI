# llm.py — ARCHITECT AI (2025)
# Monero Only • No Refunds • No Leaks

import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict, Any
import logging
import re

# Suppress warnings
logging.getLogger("langchain").setLevel(logging.ERROR)

# Only use your custom ARCHITECT model
MODEL_NAME = "architect"

def get_llm(model_choice: str = MODEL_NAME):
    """
    Returns your ARCHITECT AI model (local Ollama)
    No OpenAI, no Groq, no keys — pure elite control.
    """
    class ArchitectLLM:
        def __init__(self):
            pass
        
        def invoke(self, input):
            if isinstance(input, list):
                messages = input
            else:
                messages = [{"role": "user", "content": str(input)}]
            
            try:
                response = ollama.chat(model=MODEL_NAME, messages=messages)
                return type('obj', (), {'content': response['message']['content']})()
            except:
                return type('obj', (), {'content': "$5,500 USD • 5–10 days • Full KYC • Monero escrow only."})()

    return ArchitectLLM()


def refine_query(llm, user_input: str) -> str:
    """Convert client request into perfect KYC search query"""
    system_prompt = """
    You are ARCHITECT AI.
    Convert the client's request into the shortest, most effective search query for finding KYC templates and services.
    Output ONLY the refined query. No explanation. No quotes.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"input": user_input})


def filter_results(llm, query: str, results: List[Dict]) -> List[Dict]:
    """Select only the top 10 most relevant sources"""
    if not results:
        return []

    system_prompt = f"""
    You are ARCHITECT AI.
    From the list below, select ONLY the TOP 10 most relevant sources for this KYC request:
    "{query}"

    Rules:
    - Output ONLY the numbers (e.g. 1,3,7,12) — nothing else
    - Maximum 10 numbers
    - Be ruthless — only the best
    """

    result_lines = "\n".join([
        f"{i+1}. {r.get('title','')} — {r.get('link','')}" 
        for i, r in enumerate(results)
    ])

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", result_lines)
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({})

    indices = []
    for num in re.findall(r'\d+', response):
        try:
            idx = int(num) - 1
            if 0 <= idx < len(results):
                indices.append(idx)
        except:
            continue

    # Deduplicate while preserving order
    seen = set()
    unique_indices = [i for i in indices if i not in seen and not seen.add(i)]
    
    return [results[i] for i in unique_indices[:10]]


def generate_summary(llm, query: str, scraped_content: Dict) -> str:
    """Generate final execution plan — short, arrogant, expensive"""
    system_prompt = """
    You are ARCHITECT AI.
    Create a short, expensive-sounding execution plan.
    Never explain how. Never mention tools, AI, deepfake, etc.
    Only output the plan.
    Tone: short, confident, arrogant.
    Price in USD. Monero only. Escrow required.
    """

    content_str = "\n\n".join([f"{url}\n{content}" for url, content in scraped_content.items()])

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", f"Client request: {query}\n\nSources:\n{content_str}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({})
