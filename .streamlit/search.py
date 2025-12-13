# search.py — ARCHITECT AI (Cloud-safe OSINT search)

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SEARCH_ENGINES = [
    "https://duckduckgo.com/html/?q={query}",
]

def fetch(engine, query):
    try:
        url = engine.format(query=query)
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return [{"title": "Result", "link": url}]
    except:
        pass
    return []

def get_search_results(refined_query, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch, e, refined_query) for e in SEARCH_ENGINES]
        for f in as_completed(futures):
            results.extend(f.result())
    return results


