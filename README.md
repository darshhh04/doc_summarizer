# DocuSummarizer: AI-Powered Meeting Intelligence Platform (Code-A-Nova Internship Project)

Upload a raw meeting transcript (.txt, .docx, .pdf) and get an executive summary, key decisions with speakers, action items with owners and deadlines, risk flags with severity, and topic clusters. Export to JSON or PDF.

## Features
- Handles transcripts up to 50,000 words (speaker-safe chunking, summaries merged in steps)
- LangChain prompt chain: chunk summary, global summary, structured extraction
- Pydantic output parsing with retry (parse failures never crash the app)
- Token usage and cost estimate logged per transcript (`logs/token_log.csv`)
- Streamlit UI with tabs: Summary, Decisions, Actions, Risks
- JSON and PDF export
- ROUGE evaluation and pytest suite with mocked LLM

## Setup
1. Clone the repo and create a virtual environment:
```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
```
2. Get a free Gemini API key from https://aistudio.google.com
3. Copy `.env.example` to `.env` and add your key:
```
   GOOGLE_API_KEY=your_key_here
   GEMINI_MODEL=gemini-3.5-flash
```
   Keys are read from environment variables and never stored in the code.

## Run the app
```
streamlit run app.py
```

## Demo
1. Upload a file from `samples/` and click **Process transcript**
2. Browse the four tabs
3. Download the JSON and PDF report


## Tests and evaluation
```
pytest              # tests with a mocked LLM, no API key needed
python evaluate.py  # ROUGE on 5 samples, writes docs/evaluation_report.md
```

## Project structure
```
app.py               Streamlit UI
evaluate.py          ROUGE evaluation
src/ingestion.py     file reading and speaker normalization
src/chunking.py      speaker-aware chunking
src/summarizer.py    chunk and global summaries
src/extraction.py    structured extraction with retry
src/llm_utils.py     LLM call with retry and token logging
src/tokens.py        token and cost tracking
src/export.py        JSON and PDF export
src/schemas.py       Pydantic models
samples/             5 sample transcripts + expected summaries
docs/                prompt documentation and evaluation report
tests/               pytest tests
```

## Prompt design
See [docs/prompts.md](docs/prompts.md).