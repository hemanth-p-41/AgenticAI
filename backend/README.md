Backend — Gemini Integration

Setup

1. Install Python dependencies (prefer a virtualenv):

```bash
cd backend
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `GEMINI_API_KEY` if you have one:

```bash
cp .env.example .env
# edit .env and set GEMINI_API_KEY
```

3. Run tests (pytest):

```bash
cd backend
pytest -q
```

Notes
- The project uses `google-generativeai` to call Gemini when `GEMINI_API_KEY` is set.
- When the key is missing or the SDK fails, the service falls back to deterministic generators.
- Tests mock the Gemini client to validate both code paths.
