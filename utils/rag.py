import json, os
import numpy as np
import faiss
from utils.call_gemini import embed

def _load():
    index = faiss.read_index("store/vectors.faiss")
    with open("store/docs.json", "r", encoding="utf-8") as f:
        docs = json.load(f)
    return index, docs

def retrieve(query: str, k=4):
    index, docs = _load()
    qvec = np.array(embed([query])[0], dtype="float32").reshape(1, -1)
    faiss.normalize_L2(qvec)
    D, I = index.search(qvec, k)
    ctx = [docs[i] for i in I[0]]
    return ctx
