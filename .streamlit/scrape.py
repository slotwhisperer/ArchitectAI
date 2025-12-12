# scrape.py — ARCHITECT AI (2025)
# Monero Only • No Tor • No Darkweb • 100% Legal

import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings

warnings.filterwarnings("ignore")

# Elite 2025 rotating user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
]

def get_session():
    """Create a robust, stealthy session with retries"""
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    session.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    })
    return session

def scrape_single(url_data: dict) -> tuple:
    """
    Scrape a single public site for KYC/ID template info
    Returns (url, cleaned_content)
    """
    url = url_data.get("link", "")
    title = url_data.get("title", "No title")
    
    try:
        session = get_session()
        response = session.get(url, timeout=20, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove noise
        for element in soup(["script", "style", "nav", "header", "footer", "iframe", "noscript", "svg"]):
            element.decompose()
        
        # Extract clean text
        text = soup.get_text(separator=" ")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = " ".join(chunk for chunk in chunks if chunk)
        
        # Limit for LLM
        if len(clean_text) > 3500:
            clean_text = clean_text[:3500] + "..."
        
        result = f"SOURCE: {title}\nURL: {url}\n\n{clean_text}"
        
    except Exception as e:
        result = f"SOURCE: {title}\nURL: {url}\n\n[Content blocked or unavailable]"
    
    return url, result

def scrape_multiple(urls_data: list, max_workers: int = 8) -> dict:
    """
    Scrape multiple public sites concurrently
    Returns dict: {url: content}
    """
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(scrape_single, item): item 
            for item in urls_data
        }
        
        for future in as_completed(future_to_url):
            try:
                url, content = future.result()
                results[url] = content
            except:
                item = future_to_url[future]
                results[item.get("link", "unknown")] = f"SOURCE: {item.get('title','')}\n[Failed to retrieve]"
    
    return results
