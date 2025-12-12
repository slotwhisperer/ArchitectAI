from langchain_ollama import ChatOllama

def get_llm(model_name="architect"):
    """Return a local Ollama LLM."""
    return ChatOllama(
        model=model_name,
        base_url="http://127.0.0.1:11434",
        temperature=0.3,
    )

def refine_query(llm, query):
    """Simplified query refinement."""
    prompt = f"Refine this OSINT search query for accuracy:\n\n{query}"
    return llm.invoke(prompt).content.strip()

def filter_results(llm, query, results):
    """Filter search results using the LLM."""
    text = "\n".join(results)
    prompt = (
        f"Given the query:\n{query}\n\n"
        f"Filter these results to only the most relevant sources:\n{text}"
    )
    output = llm.invoke(prompt).content.strip()
    return output.splitlines()

def generate_summary(llm, query, scraped_data):
    """Generate final report."""
    body = "\n\n".join(scraped_data)
    prompt = (
        f"Create a concise intelligence report for query: {query}\n\n"
        f"Scraped content:\n{body}\n\n"
        f"Summarize findings and extract key insights."
    )
    return llm.invoke(prompt).content.strip()
