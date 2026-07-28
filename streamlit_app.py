"""
streamlit_app.py
------------------
Final Streamlit UI for the RAG assistant (first aid book).

It reuses the already-built vector store (created by 05_create_chroma_store.py)
and calls:
    06_retrieve_context.retrieve_context()  -> get relevant chunks
    07_prompting.build_prompt() + ask_ai()  -> get the final answer

API key handling:
    - Locally, 07_prompting.py reads OPENROUTER_API_KEY from a .env file.
    - On Streamlit Cloud, we inject the key from st.secrets into the
      "rag" module (07_prompting) at runtime, so the real key is never
      committed to the repo.

Run locally:
    streamlit run streamlit_app.py
"""

import importlib
import streamlit as st

# Python module names can't start with digits, so we import them dynamically.
retrieve_context_module = importlib.import_module("06_retrieve_context")
rag = importlib.import_module("07_prompting")  # "rag" = the prompting/LLM module

retrieve_context = retrieve_context_module.retrieve_context
build_prompt = rag.build_prompt
ask_ai = rag.ask_ai

# ---- Inject Streamlit secrets into the rag module (only fills in what's missing) ----
try:
    if not rag.OPENROUTER_API_KEY:
        rag.OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")
    rag.OPENROUTER_MODEL = st.secrets.get("OPENROUTER_MODEL", rag.OPENROUTER_MODEL)
except Exception:
    # st.secrets raises if no secrets.toml exists (e.g. running fully locally
    # with only a .env file) - that's fine, we just keep the .env values.
    pass


st.set_page_config(page_title="مساعد الإسعافات الأولية", page_icon="🩹")

st.title("🩹 مساعد الإسعافات الأولية (RAG)")
st.caption("اسأل أي سؤال عن الإسعافات الأولية، والإجابة هتكون مبنية على محتوى الكتاب فقط.")

if not rag.OPENROUTER_API_KEY:
    st.warning(
        "لا يوجد OPENROUTER_API_KEY. أضِفه في ملف .env محليًا، "
        "أو في Streamlit secrets عند النشر."
    )

question = st.text_input("اكتب سؤالك هنا:", placeholder="مثال: ما هي أعراض الكسر؟")
n_results = st.slider("عدد المقاطع المسترجعة (context chunks)", 1, 8, 3)

if st.button("اسأل") and question.strip():
    with st.spinner("جاري البحث في الكتاب..."):
        retrieved = retrieve_context(question, n_results=n_results)

    with st.spinner("جاري توليد الإجابة..."):
        prompt = build_prompt(question, retrieved)
        try:
            answer = ask_ai(prompt)
        except RuntimeError as e:
            st.error(str(e))
            answer = None

    if answer:
        st.subheader("الإجابة")
        st.write(answer)

        st.subheader("📚 المصادر (Sources) اللي اتبنت عليها الإجابة")
        for i, (chunk, distance) in enumerate(retrieved):
            with st.expander(f"مصدر {i + 1} (distance={distance:.4f})" if distance is not None else f"مصدر {i + 1}"):
                st.write(chunk)
