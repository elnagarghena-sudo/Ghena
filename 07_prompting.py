"""
07_prompting.py
----------------
Step 7 of the RAG pipeline: build the final prompt from the retrieved chunks,
send it to an LLM through OpenRouter, and return the answer.

IMPORTANT (API key rules):
    - Never hard-code your real API key here.
    - Locally: put it in a .env file (which is git-ignored) as OPENROUTER_API_KEY=...
    - On Streamlit Cloud: it is injected from st.secrets by streamlit_app.py,
      which overwrites OPENROUTER_API_KEY / OPENROUTER_MODEL on this module at runtime.

Run (quick test, needs OPENROUTER_API_KEY set in your environment/.env):
    python 07_prompting.py
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # loads variables from a local .env file, if present

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def build_prompt(question: str, context_chunks) -> str:
    """
    context_chunks can be a list of strings, or a list of (chunk, distance) tuples
    coming from 06_retrieve_context.retrieve_context().
    """
    texts = [c[0] if isinstance(c, (list, tuple)) else c for c in context_chunks]
    context_text = "\n\n".join(texts)

    prompt = f"""أجب على السؤال بالاعتماد فقط على السياق الموجود أدناه.
إذا لم تجد الإجابة في السياق، قل أنك لا تعرف.
اذكر دائمًا أي جزء من السياق استخدمته في إجابتك.

السياق:
{context_text}

السؤال: {question}

الإجابة:"""
    return prompt


def ask_ai(prompt: str) -> str:
    """
    Send the prompt to the configured OpenRouter model and return the answer text.
    Raises a clear RuntimeError if the API key is missing or the request fails.
    """
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Set it in a local .env file, "
            "or configure it in Streamlit secrets when deployed."
        )

    response = requests.post(
        url=OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"OpenRouter request failed ({response.status_code}): {response.text}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    from importlib import import_module

    retrieve_module = import_module("06_retrieve_context")

    test_question = "ما هي أعراض الكسر؟"
    retrieved_chunks = retrieve_module.retrieve_context(test_question)
    test_prompt = build_prompt(test_question, retrieved_chunks)
    print(test_prompt[:800])
    print("\n--- Answer ---")
    print(ask_ai(test_prompt))
