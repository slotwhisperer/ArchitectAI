# llm.py — ARCHITECT AI Edition (2025)
# Works perfectly with Ollama + Streamlit Cloud (when using local Ollama via tunnel)

import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# No API keys needed — uses your local Ollama model "architect"
def get_llm(model_choice="architect"):
    """
    Returns a LangChain-compatible LLM that talks to your local Ollama model.
    We only use one model: 'architect' (your custom 8B/70B model)
    """
    class OllamaLLM:
        def __init__(self, model):
            self.model = model

        def invoke(self, input):
            if isinstance(input, list):
                messages = input
            else:
                messages = [{"role": "user", "content": str(input)}]

            response = ollama.chat(model=self.model, messages=messages)
            return type('obj(content=response['message']['content'])

        def stream(self, input):
            if isinstance(input, list):
                messages = input
            else:
                messages = [{"role": "user", "content": str(input)}]

            for chunk in ollama.chat(model=self.model, messages=messages, stream=True):
                yield chunk['message']['content']

    # Fake type for LangChain compatibility
    class typeobj:
        def __init__(self, content):
            self.content = content

    return OllamaLLM(model=model_choice)


def refine_query(llm, user_input):
    """Turn a client request into a perfect search query"""
    system_prompt = """
    You are ARCHITECT AI. Convert the client's request into the shortest, most effective search query possible.
    Output ONLY the refined query. No explanation. No quotes.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"input": user_input})


def filter_results(llm, query, results):
    """Pick the top 10 most relevant results"""
    if not results:
        return []

    system_prompt = f"""
    You are ARCHITECT AI. From the list below, select the TOP 10 most relevant results for this request:
    "{query}"

    Rules:
    - Only output the numbers (e.g. 1,3,7,12)
    - Maximum 10 numbers
    - Nothing else
    """

    result_lines = "\n".join([f"{i+1}. {r.get('title', '')} — {r.get('link', '')}" 
                             for i, r in enumerate(results)])

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
    return [results[i] for i in indices[:10]]


def generate_summary(llm, query, scraped_content):
    """Generate final execution plan for the client"""
    system_prompt = """
    You are ARCHITECT AI.
    Create a short, expensive-sounding execution plan.
    Never explain how anything works.
    Never mention tools, AI, deepfake, forge, swap,
