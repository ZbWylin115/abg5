"""
Generator API routes.

Milestone 1: returns placeholder content loaded from a JSON file, just
to prove the frontend <-> backend wiring. Real generation logic will
replace the random-pick-from-list behavior later.
"""

import json
import random
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/api/generator", tags=["generator"])

CONTENT_PATH = Path(__file__).parent.parent / "data" / "generator_content.json"


def _load_content() -> dict:
    with open(CONTENT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/random")
def get_random_entry():
    """Return one random placeholder entry."""
    content = _load_content()
    entry = random.choice(content["placeholders"])
    return {"entry": entry}


@router.get("/all")
def get_all_entries():
    """Return every placeholder entry (useful for debugging in-browser)."""
    content = _load_content()
    return {"entries": content["placeholders"]}
