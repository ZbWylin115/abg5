# ABG Bible

Full-stack web app. FastAPI backend serves both the API and the static
frontend directly — one deployable app, no separate frontend server.

## Run locally

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Then open http://127.0.0.1:8000

## Project layout

- `app/main.py` — FastAPI app entrypoint, mounts static files, serves pages
- `app/database.py` — SQLite connection + schema init
- `app/routers/` — API route modules (one per feature)
- `app/data/` — JSON files for expandable/editable content
- `app/static/` — HTML/CSS/JS frontend, served directly by FastAPI
