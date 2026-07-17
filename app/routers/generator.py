"""
Generator API routes.

Milestone 2: replaces the placeholder random-pick logic with the real
knowledge-base-driven matching engine. Culture is never a scoring
input - it only attaches an optional read-only info panel.
"""

from fastapi import APIRouter, Query

from app import matching
from app.schemas import GenerateResult

router = APIRouter(prefix="/api", tags=["generator"])


@router.get("/generate", response_model=GenerateResult)
def generate(
    archetypes: list[str] = Query(default=[], description="Up to 2 archetype ids"),
    city: str | None = Query(default=None),
    venue: str | None = Query(default=None),
    interest_level: str | None = Query(default=None),
    boldness_level: str | None = Query(default=None),
    culture: str | None = Query(default=None),
    include_cultural_context: bool = Query(default=False),
):
    archetypes = archetypes[:2]  # enforce "up to 2" server-side too

    result = matching.build_generation(
        archetypes=archetypes,
        city=city,
        venue=venue,
        interest_level=interest_level,
        boldness_level=boldness_level,
        culture=culture,
        include_cultural_context=include_cultural_context,
    )
    return result
