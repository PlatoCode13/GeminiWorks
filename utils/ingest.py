import os, glob, json
import numpy as np
import faiss
from utils.call_gemini import embed

def chunk_text(txt: str, chunk=800, overlap=150):
    """Simple overlap chunking so answers have context."""
    pieces = []
    i = 0
    while i < len(txt):
        pieces.append(txt[i:i+chunk])
        i += chunk - overlap
    return pieces

def load_and_chunk(pattern="data/*.md"):
    """Read docs and split into chunks with source metadata."""
    docs = []
    for path in glob.glob(pattern):
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        for ch in chunk_text(raw):
            docs.append({"text": ch, "source": os.path.basename(path)})
    return docs

def build_faiss_index(docs, store_dir="store"):
    """Create FAISS index + save docs metadata in JSON."""
    os.makedirs(store_dir, exist_ok=True)
    texts = [d["text"] for d in docs]
    vectors = np.array(embed(texts), dtype="float32")
    # Normalize to use cosine similarity with inner product
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, os.path.join(store_dir, "vectors.faiss"))
    with open(os.path.join(store_dir, "docs.json"), "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

def ensure_index():
    """Build once; skip if already exists."""
    if not os.path.exists("store/vectors.faiss"):
        docs = load_and_chunk()
        build_faiss_index(docs)
        return True
    return False
