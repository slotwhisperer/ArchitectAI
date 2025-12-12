# scrape.py — ARCHITECT AI Edition (2025)
# Safe, fast, legal web scraping for KYC template research

import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings

warnings.filterwarnings("ignore")

# Elite rotating user agents (2025 browsers)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
]

def get_session():
    """Create a robust session with retries and random headers"""
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    session.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    })
    return session

def scrape_single(url_data):
    """
    Scrape a single public site for KYC/ID template info.
    Returns (url, cleaned_text)
    """
    url = url_data['link']
    title = url_data.get('title', 'No title')
    
    try:
        session = get_session()
        response = session.get(url, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove junk
        for element in soup(["script", "style", "nav", "header", "footer", "iframe", "noscript"]):
            element.decompose()
        
        # Extract meaningful text
        text = soup.get_text(separator=" ")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)
        
        # Limit length for LLM
        if len(text) > 3000:
            text = text[:3000] + "..."
            
        result = f"TITLE: {title}\nURL: {url}\n\n{text}"
        
    except Exception:
        result = f"TITLE: {title}\nURL: {url}\n\n[Content unavailable or blocked]"
    
    return url, result

def scrape_multiple(urls_data, max_workers=8):
    """
    Scrape multiple public sites concurrently.
    Returns dict: {url: scraped_text}
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
                url = future_to_url[future]['link']
                results[url] = f"TITLE: {future_to_url[future].get('title','Unknown')}\nURL: {url}\n\n[Failed to load]"
    
    return results
