import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .scraper import safe_filename
from .config import CACHE_DIR

class Retriever:
    def __init__(self):
        self.vectorizer = None

    def load_sources(self, sources_file):
        with open(sources_file, 'r', encoding='utf-8') as f:
            return [l.strip() for l in f if l.strip()]

    def _load_cached_texts(self, urls):
        passages = []
        for url in urls:
            fname = os.path.join(CACHE_DIR, safe_filename(url) + '.txt')
            if os.path.exists(fname):
                with open(fname, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Разбиваем на абзацы
                    for para in content.split('\n\n'):
                        para = para.strip()
                        if para:
                            passages.append({'url': url, 'text': para})
        return passages

    def retrieve(self, question, urls, top_k=3):
        passages = self._load_cached_texts(urls)
        texts = [p['text'] for p in passages]
        if not texts:
            return []
        self.vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1,2))
        X = self.vectorizer.fit_transform(texts)
        qv = self.vectorizer.transform([question])
        sims = cosine_similarity(qv, X)[0]
        top_idx = sims.argsort()[::-1][:top_k]
        return [passages[i] for i in top_idx]