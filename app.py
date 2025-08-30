import os
import pandas as pd
import streamlit as st

from utils.ingest import ensure_index
from utils.rag import retrieve
from utils.prompts import DOC_QA_PROMPT, WORKSHOP_SUMMARY_PROMPT, WRANGLING_PROMPT
from utils.call_gemini import generate

st.set_page_config(page_title="GeminiWorks", layout="wide")
st.title("GeminiWorks – Engineering Automation Mini Suite")

# 1) build index once (first run)
with st.spinner("Preparing document index..."):
    first = ensure_index()
    if first:
        st.success("Index built.")
    else:
        st.info("Index found. Ready.")

tab1, tab2, tab3 = st.tabs(["📘 Doc Q&A", "📝 Workshop Summarizer", "🧹 Data-Wrangling Assistant"])

# ---------- Tab 1: Doc Q&A ----------
with tab1:
    st.subheader("Ask questions about mock SRM/AMM docs")
    q = st.text_input("Your question", placeholder="e.g., What torque for fastener FZ-28?")
    if st.button("Answer", key="qa_btn") and q.strip():
        ctx = retrieve(q, k=4)
        # format context for prompt
        ctx_str = "\n\n---\n".join([f"[{c['source']}] {c['text']}" for c in ctx])
        prompt = DOC_QA_PROMPT.format(question=q, context=ctx_str)
        with st.spinner("Thinking..."):
            answer = generate(prompt)
        st.markdown(answer)

# ---------- Tab 2: Summarizer ----------
with tab2:
    st.subheader("Turn notes/transcripts into key points + action items")
    notes = st.text_area("Paste notes here", height=220,
                         placeholder="Bullets, messy text, or transcript...")
    if st.button("Summarize", key="sum_btn") and notes.strip():
        prompt = WORKSHOP_SUMMARY_PROMPT.format(notes=notes[:6000])
        with st.spinner("Summarizing..."):
            out = generate(prompt)
        st.markdown(out)

# ---------- Tab 3: Data Wrangling ----------
with tab3:
    st.subheader("Upload a CSV → get cleaning suggestions + code")
    f = st.file_uploader("Upload CSV", type=["csv"])
    if f is not None:
        df = pd.read_csv(f)
        st.write("Preview (first 20 rows):")
        st.dataframe(df.head(20))
        # create schema + sample for prompt
        schema = ", ".join([f"{c}:{df[c].dtype}" for c in df.columns])
        sample = df.head(5).to_csv(index=False)
        if st.button("Suggest fixes + code", key="wrangle_btn"):
            prompt = WRANGLING_PROMPT.format(schema=schema, sample=sample)
            with st.spinner("Analyzing..."):
                out = generate(prompt)
            st.markdown(out)
            st.info("Copy the Pandas/SQL code above into your environment to run it.")
