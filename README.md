# GeminiWorks — Engineering Automation Mini Suite 🚀

**GeminiWorks** is a small, practical demo showing how **Google Gemini** can automate day-to-day engineering workflows.  
It includes a Streamlit app with three tabs:

1) **Doc Q&A** — Ask questions over mock SRM/AMM docs; answers include **citations**.  
2) **Workshop Summarizer** — Paste notes/transcripts → get **key points + JSON action items**.  
3) **Data-Wrangling Assistant** — Upload a CSV → get **data-quality findings + ready-to-run Pandas & SQL**.

Designed to mirror tasks from roles like *A320 Chief Engineering Digitalization Team* (data wrangling, automation, clear communication).

---

## ✨ Features
- RAG over local markdown docs with embeddings + retrieval
- Clean, short prompts tuned for actionable outputs
- Token/rate-limit aware (uses `gemini-1.5-flash` by default, trims context, caches)
- Simple, readable code with utilities split by function

---

## 📂 Project Structure
```
GeminiWorks/
app.py
requirements.txt
.gitignore
data/
mock_srm.md
mock_amm.md
sample_maintenance.csv
store/ # created at runtime for index + metadata
utils/
call_gemini.py # model calls, retry/backoff, embeddings
ingest.py # chunking + FAISS index build
rag.py # retrieval helper
prompts.py # prompt templates
```


---

## 🧰 Requirements
- Python **3.10+**
- A **Gemini API key** (Google AI Studio)

---

## ⚙️ Setup

```bash
# clone
git clone https://github.com/PlatoCode13/GeminiWorks.git
cd GeminiWorks

# create & activate venv
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# install deps
pip install -r requirements.txt
````
Create a .env file in the project root:
````
GEMINI_API_KEY=YOUR_REAL_KEY
# optional: pick the lighter model with higher free limits
GEMINI_MODEL=gemini-1.5-flash

````
▶️ Run

````
streamlit run app.py
````
App opens at http://localhost:8501.

Try it quickly:

Doc Q&A: “What torque range for fastener FZ-28?”

Summarizer: paste a few lines of notes; click Summarize.

Wrangling: upload data/sample_maintenance.csv; click Suggest fixes + code.



🧪 Demo Notes / Prompts

Workshop Summarizer sample:

````
A320 MAP weekly sync – 15:00–15:45

• KPI dashboard refresh 9–11 min; target <5.
• 14 rows missing torque values; likely CSV export issue.
• Need SharePoint how-to for self-service filters.
• Engineers request quick search for SRM torque ranges (FZ-28, FZ-30).
• Pilot "GeminiWorks" next Tuesday.
Owners: Sara (runtime), Leon (CSV fix), Monjurul (how-to + demo)
Deadlines: CSV Fri, how-to Mon, demo Tue
````
Doc Q&A questions:

How do I troubleshoot HYD_023 low pressure?

What’s the safety step before working near flaps?

What to check if torque exceeds limit?

🧠 Models, Rate Limits & Reliability

Default model: gemini-1.5-flash for speed + generous free tier.

You can switch to gemini-1.5-pro per call if you need deeper reasoning.

The app:

trims context (MAX_CTX_CHARS)

retrieves fewer chunks (k=2)

caches identical prompts

retries on 429 with exponential backoff

If you still hit 429:

Lower input size (shorter notes, fewer CSV rows)

Wait a few seconds between runs

Consider enabling billing or using an additional key for heavy testing

🔒 Safety & Data

Uses synthetic SRM/AMM text; do not ingest proprietary docs.

.env and runtime store/ index are excluded from Git via .gitignore.

🛠️ Tech Stack

Streamlit, Pandas

Google Gemini API (google-generativeai)

FAISS for vector search (faiss-cpu)

Python-dotenv for secrets



