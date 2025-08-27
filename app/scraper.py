import os
import requests
from bs4 import BeautifulSoup
from .config import CACHE_DIR
import hashlib

def safe_filename(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()

def fetch_text(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    for s in soup(['script','style','noscript']):
        s.decompose()
    title = soup.title.string if soup.title else ''
    text = ' '.join(p.get_text(separator=' ', strip=True) for p in soup.find_all(['p','h1','h2','h3','li']))
    return title, text

def ensure_cached_texts(urls, cache_dir=CACHE_DIR):
    os.makedirs(cache_dir, exist_ok=True)
    for url in urls:
        fname = os.path.join(cache_dir, safe_filename(url) + '.txt')
        if not os.path.exists(fname):
            try:
                title, text = fetch_text(url)
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(f"{url}\n{title}\n\n{text}")
            except Exception as e:
                print(f"Ошибка при загрузке {url}: {e}")