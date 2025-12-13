# search.py — ARCHITECT AI
# Dark web search aggregation with Tor + graceful fallback
# Compatible with existing UI + scrape pipeline

import requests
import random
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings

warnings.filterwarnings("ignore")

# -----------------------------
# USER AGENTS
# -----------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
]

# -----------------------------
# ONION SEARCH ENGINES
# -----------------------------
SEARCH_ENGINE_ENDPOINTS = [
    "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={query}",  # Ahmia
    "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q={query}",  # OnionLand
    "http://darkhuntyla64h75a3re5e2l3367lqn7ltmdzpgmr6b4nbz3q2iaxrid.onion/search?q={query}",  # DarkHunt
    "http://iy3544gmoeclh5de6gez2256v6pjh4omhpqdh2wpeeppjtvqmjhkfwad.onion/torgle/?query={query}",  # Torgle
    "http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion/search?q={query}",  # Tor66
]

# -----------------------------
# TOR PROXIES
# -----------------------------
def get_tor_proxies():
    return {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050",
    }

# -----------------------------
# FETCH RESULTS FROM ONE ENGINE
# -----------------------------
def fetch_search_results(endpoint: str, query: str):
    url = endpoint.format(query=query)
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            proxies=get_tor_proxies(),
            timeout=25,
        )
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for a in soup.find_all("a"):
            href = a.get("href")
            title = a.get_text(strip=True)

            if not href or not title:
                continue

            match = re.search(r"https?://[a-zA-Z0-9\-]+\.onion[^\"'\s]*", href)
            if match:
                results.append({
                    "title": title[:120],
                    "link": match.group(0)
                })

        return results

    except Exception:
        # Tor not running / blocked / timeout
        return []

# -----------------------------
# PUBLIC API — USED BY UI
# -----------------------------
def get_search_results(refined_query: str, max_workers: int = 5):
    """
    Returns:
        List[dict] -> [{ "title": str, "link": str }]
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_search_results, endpoint, refined_query)
            for endpoint in SEARCH_ENGINE_ENDPOINTS
        ]

        for future in as_completed(futures):
            try:
                results.extend(future.result())
            except Exception:
                continue

    # Deduplicate by URL
    seen = set()
    unique_results = []

    for item in results:
        link = item.get("link")
        if link and link not in seen:
            seen.add(link)
            unique_results.append(item)

    return unique_results

