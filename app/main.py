"""
ABG Bible - FastAPI entrypoint.

Serves the API routers AND the static frontend from one process, so
this is a single deployable app.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import generator, knowledge

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
PAGES_DIR = STATIC_DIR / "pages"

app = FastAPI(title="ABG Bible")

# --- API routers ---
app.include_router(generator.router)
app.include_router(knowledge.router)

# --- Static assets (css/js) ---
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def on_startup():
    init_db()


# --- Page routes (serve raw HTML files directly) ---
@app.get("/")
def serve_index():
    return FileResponse(PAGES_DIR / "index.html")


@app.get("/generator")
def serve_generator():
    return FileResponse(PAGES_DIR / "generator.html")


@app.get("/rules")
def serve_rules():
    return FileResponse(PAGES_DIR / "rules.html")
