# search.py — ARCHITECT AI Edition (2025)
# Safe, fast, legal web search for KYC templates & services

import requests
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings

warnings.filterwarnings("ignore")

# Elite 2025 User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
]

# Public search engines & forums for KYC templates (all legal)
SEARCH_QUERIES = [
    "https://www.google.com/search?q={query}",
    "https://duckduckgo.com/html/?q={query}",
    "https://www.bing.com/search?q={query}",
    "https://search.brave.com/search?q={query}",
]

# Keywords to boost relevance
KYC_KEYWORDS = [
    "template", "PSD", "ID template", "DL template", "passport template",
    "selfie + scan", "KYC service", "verified account", "document service",
    "novelty ID", "fake ID template", "editable PSD", "high quality scan"
]

def build_search_query(refined):
    """Add KYC keywords for better results"""
    extra = " ".join(random.sample(KYC_KEYWORDS, 4))
    return f"{refined} {extra} site:-facebook.com site:-instagram.com site:-tiktok.com"

def safe_get(url, timeout=15):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        r.raise_for_status()
        return r.text
    except:
        return None

def extract_results(html, source="google"):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    if "google" in source:
        for g in soup.find_all('div', class_='g'):
            a = g.find('a')
            if a and a.h3:
                link = a['href']
                title = a.h3.text
                if link.startswith('/url?'):
                    link = requests.utils.unquote(link.split('/url?q=')[1].split('&')[0])
                if any(bad in link for bad in ["facebook", "instagram", "tiktok", "youtube"]):
                    continue
                results.append({"title": title, "link": link})

    elif "duckduckgo" in source:
        for result in soup.find_all('article'):
            a = result.find('a', {'data-testid': 'result-title-a'})
            if a:
                results.append({"title": a.text, "link": a['href']})

    elif "bing" in source:
        for li in soup.find_all('li', class_='b_algo'):
            a = li.find('a')
            if a:
                results.append({"title": a.text, "link": a['href']})

    return results[:20]  # Limit to top 20

def get_search_results(refined_query, max_workers=6):
    """Search public web for KYC templates & services"""
    query = build_search_query(refined_query)
    encoded = requests.utils.quote(query)
    search_urls = [url for url in SEARCH_QUERIES]

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_engine = {
            executor.submit(safe_get, url.format(query=encoded)): name
            for name, url in zip(["google", "duckduckgo", "bing", "brave"], search_urls)
        }

        for future in as_completed(future_to_engine):
            html = future.result()
            if html:
                engine = future_to_engine[future]
                results.extend(extract_results(html, engine))

    # Deduplicate
    seen = set()
    unique = []
    for r in results:
        if r["link"] not in seen:
            seen.add(r["link"])
            unique.append(r)

    return unique[:30]  # Return top 30 unique results
