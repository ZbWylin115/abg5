"""
Loads and caches the JSON knowledge base for ABG Bible.

Everything content-related lives in app/data/knowledge/*.json.
Adding new archetypes, cities, venues, or examples means editing those
files - no application code changes required.
"""

import json
from pathlib import Path
from functools import lru_cache

KNOWLEDGE_DIR = Path(__file__).parent / "data" / "knowledge"


def _load(filename: str) -> dict:
    path = KNOWLEDGE_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_archetypes() -> list[dict]:
    return _load("archetypes.json")["archetypes"]


@lru_cache(maxsize=1)
def get_cultures() -> list[dict]:
    return _load("cultures.json")["cultures"]


@lru_cache(maxsize=1)
def get_cultural_context_general() -> list[str]:
    return _load("cultural_context.json")["general_guidelines"]


@lru_cache(maxsize=1)
def get_cities() -> list[dict]:
    return _load("cities.json")["cities"]


@lru_cache(maxsize=1)
def get_venues() -> list[dict]:
    return _load("venues.json")["venues"]


@lru_cache(maxsize=1)
def get_interest_levels() -> list[dict]:
    return _load("interest_levels.json")["interest_levels"]


@lru_cache(maxsize=1)
def get_boldness_levels() -> list[dict]:
    return _load("boldness_levels.json")["boldness_levels"]


@lru_cache(maxsize=1)
def get_conversation_examples() -> list[dict]:
    return _load("conversation_examples.json")["examples"]


@lru_cache(maxsize=1)
def get_date_ideas() -> list[dict]:
    return _load("date_ideas.json")["date_ideas"]


@lru_cache(maxsize=1)
def get_rules() -> list[dict]:
    return _load("rules.json")["rules"]


def find_by_id(items: list[dict], item_id: str) -> dict | None:
    return next((item for item in items if item.get("id") == item_id), None)


def clear_cache() -> None:
    """Useful in tests or if content is hot-reloaded."""
    for fn in (
        get_archetypes,
        get_cultures,
        get_cultural_context_general,
        get_cities,
        get_venues,
        get_interest_levels,
        get_boldness_levels,
        get_conversation_examples,
        get_date_ideas,
        get_rules,
    ):
        fn.cache_clear()
