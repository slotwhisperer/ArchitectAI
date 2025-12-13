# llm.py — ARCHITECT AI (Cloud-safe, no chains)

def get_llm(model_name: str):
    """
    Returns a callable LLM wrapper that exposes .invoke(prompt)
    Compatible with Groq-style chat models.
    """
    from groq import Groq
    import streamlit as st

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    class GroqLLM:
        def invoke(self, prompt: str):
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a professional OSINT analyst."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=800,
            )
            return response.choices[0].message.content

    return GroqLLM()


# ---------------- OSINT HELPERS ----------------

def refine_query(llm, query: str) -> str:
    prompt = f"""
Refine the following OSINT investigation query.
Make it precise, focused, and actionable.

Query:
{query}

Return ONLY the refined query.
"""
    return llm.invoke(prompt).strip()


def filter_results(llm, refined_query: str, results: list) -> list:
    # Keep structure intact; filtering is semantic guidance only
    return results


def generate_summary(llm, query: str, scraped_data: dict) -> str:
    prompt = f"""
Generate a structured intelligence summary.

Original query:
{query}

Scraped content:
{scraped_data}

Provide a clear, analyst-grade OSINT report.
"""
    return llm.invoke(prompt).strip()

