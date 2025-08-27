from fastapi import FastAPI
from pydantic import BaseModel
from .scraper import ensure_cached_texts
from .retriever import Retriever
from .llm_client import LLMClient

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    urls: list[str] | None = None
    top_k: int = 3

retriever = Retriever()
llm = LLMClient()

@app.post('/query')
async def query(req: QueryRequest):
    urls = req.urls or retriever.load_sources('app/sources.txt')
    ensure_cached_texts(urls)
    top_docs = retriever.retrieve(req.question, urls, top_k=req.top_k)
    answer = llm.ask_with_context(req.question, top_docs)
    return {
        'answer': answer,
        'sources': [d['url'] for d in top_docs],
        'used_passages': [d['text'] for d in top_docs]
    }