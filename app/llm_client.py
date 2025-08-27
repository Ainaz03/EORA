import os
from .config import MOCK_MODE, OPENAI_API_KEY

if not MOCK_MODE:
    import openai
    openai.api_key = OPENAI_API_KEY

class LLMClient:
    def ask_with_context(self, question, docs):
        if MOCK_MODE:
            # Заглушка для тестирования без API ключа
            return f"[Mock answer] Вопрос: {question} — используется {len(docs)} источников."
        else:
            system = "You are an assistant that answers customer questions using only the provided sources. Cite sources by URL in the response when possible."
            context = '\n---\n'.join([f"URL: {d['url']}\n{d['text'][:1000]}" for d in docs])
            prompt = f"{system}\n\nContext:\n{context}\n\nUser question: {question}\n\nAnswer concisely and include Sources list."
            res = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role':'system','content':system},{'role':'user','content':prompt}],
                max_tokens=500
            )
            return res.choices[0].message.content