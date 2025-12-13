# llm.py — ARCHITECT AI (Stable, No LangChain Chains)

from groq import Groq

def get_llm(model_name: str):
    # Groq client (Streamlit Cloud compatible)
    return Groq()

def refine_query(llm, query: str) -> str:
    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Rewrite the user query into a concise OSINT investigation query."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0.2,
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()

def filter_results(llm, refined_query: str, results: list) -> list:
    # Light filtering: keep top N results
    return results[:10]

def generate_summary(llm, original_query: str, scraped_data: dict) -> str:
    content = "\n\n".join(scraped_data.values())

    response = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate a professional intelligence report. "
                    "Be factual, structured, and concise."
                )
            },
            {
                "role": "user",
                "content": f"Query: {original_query}\n\nData:\n{content}"
            }
        ],
        temperature=0.3,
        max_tokens=700,
    )

    return response.choices[0].message.content.strip()
