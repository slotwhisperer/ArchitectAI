# llm.py — ARCHITECT AI (NO LangChain, Cloud Safe)

from groq import Groq
import streamlit as st


def get_llm(model_name: str):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    class LLM:
        def invoke(self, prompt: str) -> str:
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

    return LLM()


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
    # No semantic filtering yet – keep results intact
    return results


def generate_summary(llm, query: str, scraped_data: dict) -> str:
    prompt = f"""
Generate a structured intelligence report.

Original query:
{query}

Scraped data:
{scraped_data}

Produce a clear, analyst-grade OSINT summary.
"""
    return llm.invoke(prompt).strip()

