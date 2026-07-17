"""Read-only endpoints that expose the knowledge base to the frontend."""

from fastapi import APIRouter

from app import knowledge

router = APIRouter(prefix="/api", tags=["knowledge"])


@router.get("/archetypes")
def list_archetypes():
    return {"archetypes": knowledge.get_archetypes()}


@router.get("/cultures")
def list_cultures():
    return {"cultures": knowledge.get_cultures()}


@router.get("/cities")
def list_cities():
    return {"cities": knowledge.get_cities()}


@router.get("/venues")
def list_venues():
    return {"venues": knowledge.get_venues()}


@router.get("/interest-levels")
def list_interest_levels():
    return {"interest_levels": knowledge.get_interest_levels()}


@router.get("/boldness-levels")
def list_boldness_levels():
    return {"boldness_levels": knowledge.get_boldness_levels()}


@router.get("/rules")
def list_rules():
    return {"rules": knowledge.get_rules()}
