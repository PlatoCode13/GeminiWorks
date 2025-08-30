import os
from dotenv import load_dotenv
import google.generativeai as genai

# Choose "gemini-1.5-pro" for best quality, "gemini-1.5-flash" for speed/cost
GEN_MODEL = "gemini-1.5-pro"
EMB_MODEL = "text-embedding-004"

def _configure():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in .env")
    genai.configure(api_key=api_key)

def generate(prompt: str) -> str:
    """Return plain text from Gemini for a given prompt string."""
    _configure()
    model = genai.GenerativeModel(GEN_MODEL)
    resp = model.generate_content(prompt)
    # Safety: model may return candidates; we take text if present
    return getattr(resp, "text", "").strip()

def embed(texts: list[str]) -> list[list[float]]:
    """Return embeddings (list of vectors) for a list of strings."""
    _configure()
    # Batch embeddings to be safe with long lists
    out = []
    for t in texts:
        e = genai.embed_content(model=EMB_MODEL, content=t)
        out.append(e["embedding"])
    return out
