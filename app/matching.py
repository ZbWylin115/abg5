"""
First-pass matching engine.

No AI here - this scores knowledge-base entries against the user's
selections and randomly picks among the top-scoring results so output
isn't identical every time.

Culture is intentionally NOT a scoring input. It never changes which
opening line, follow-up, topic, or avoid-tip gets selected. If the user
opts in, cultural info is attached separately as a read-only panel.
"""

import random

from app import knowledge


def _matches(field_values: list[str], selected: str | None) -> bool:
    """A knowledge entry field matches a selection if it's a wildcard
    ('any'/empty) or contains the selected value. No selection made by
    the user (None) also counts as an automatic match."""
    if selected is None:
        return True
    if not field_values:
        return True
    normalized = [v.lower() for v in field_values]
    if "any" in normalized:
        return True
    return selected.lower() in normalized


def _score_entry(entry: dict, archetypes: list[str], city: str | None,
                  venue: str | None, interest_level: str | None,
                  boldness_level: str | None) -> int:
    score = 0

    entry_archetypes = entry.get("archetypes", [])
    if "any" in [a.lower() for a in entry_archetypes]:
        score += 1
    else:
        overlap = set(a.lower() for a in entry_archetypes) & set(a.lower() for a in archetypes)
        if overlap:
            score += 2 * len(overlap)
        elif archetypes:
            # no overlap at all with a non-wildcard entry -> not a candidate
            return -1

    if not _matches(entry.get("cities", []), city):
        return -1
    if "any" not in [c.lower() for c in entry.get("cities", [])] and city:
        score += 1

    if not _matches(entry.get("venues", []), venue):
        return -1
    if "any" not in [v.lower() for v in entry.get("venues", [])] and venue:
        score += 1

    if not _matches(entry.get("interest_levels", []), interest_level):
        return -1
    if "any" not in [i.lower() for i in entry.get("interest_levels", [])] and interest_level:
        score += 1

    if not _matches(entry.get("boldness_levels", []), boldness_level):
        return -1
    if "any" not in [b.lower() for b in entry.get("boldness_levels", [])] and boldness_level:
        score += 1

    return score


def _best_matches(entries: list[dict], entry_type: str | None, archetypes: list[str],
                   city: str | None, venue: str | None, interest_level: str | None,
                   boldness_level: str | None) -> list[dict]:
    candidates = []
    for entry in entries:
        if entry_type and entry.get("type") != entry_type:
            continue
        score = _score_entry(entry, archetypes, city, venue, interest_level, boldness_level)
        if score >= 0:
            candidates.append((score, entry))

    if not candidates:
        return []

    top_score = max(c[0] for c in candidates)
    return [entry for score, entry in candidates if score == top_score]


def pick_one(entries: list[dict], entry_type: str, archetypes: list[str],
              city: str | None, venue: str | None, interest_level: str | None,
              boldness_level: str | None) -> dict | None:
    top = _best_matches(entries, entry_type, archetypes, city, venue, interest_level, boldness_level)
    return random.choice(top) if top else None


def pick_several(entries: list[dict], entry_type: str, archetypes: list[str],
                  city: str | None, venue: str | None, interest_level: str | None,
                  boldness_level: str | None, limit: int = 3) -> list[dict]:
    top = _best_matches(entries, entry_type, archetypes, city, venue, interest_level, boldness_level)
    random.shuffle(top)
    return top[:limit]


def pick_date_idea(date_ideas: list[dict], archetypes: list[str], city: str | None) -> dict | None:
    candidates = []
    for idea in date_ideas:
        idea_archetypes = [a.lower() for a in idea.get("archetypes", [])]
        idea_cities = [c.lower() for c in idea.get("cities", [])]

        archetype_ok = ("any" in idea_archetypes) or (not archetypes) or \
            bool(set(idea_archetypes) & set(a.lower() for a in archetypes))
        city_ok = ("any" in idea_cities) or (not city) or (city.lower() in idea_cities)

        if archetype_ok and city_ok:
            candidates.append(idea)

    return random.choice(candidates) if candidates else None


def build_generation(archetypes: list[str], city: str | None, venue: str | None,
                      interest_level: str | None, boldness_level: str | None,
                      culture: str | None, include_cultural_context: bool) -> dict:
    examples = knowledge.get_conversation_examples()

    opening = pick_one(examples, "opening", archetypes, city, venue, interest_level, boldness_level)
    follow_up = pick_one(examples, "follow_up", archetypes, city, venue, interest_level, boldness_level)
    topics = pick_several(examples, "topic", archetypes, city, venue, interest_level, boldness_level, limit=3)
    avoid = pick_several(examples, "avoid", archetypes, city, venue, interest_level, boldness_level, limit=2)
    date_idea = pick_date_idea(knowledge.get_date_ideas(), archetypes, city)

    result = {
        "opening_line": opening["text"] if opening else None,
        "follow_up": follow_up["text"] if follow_up else None,
        "topics": [t["text"] for t in topics],
        "avoid": [a["text"] for a in avoid],
        "date_idea": date_idea["text"] if date_idea else None,
        "cultural_context": None,
    }

    if include_cultural_context and culture:
        culture_entry = knowledge.find_by_id(knowledge.get_cultures(), culture)
        if culture_entry:
            result["cultural_context"] = {
                "display_name": culture_entry["display_name"],
                "general_guidelines": knowledge.get_cultural_context_general(),
                "conversation_topics": culture_entry.get("conversation_topics", []),
                "respect_notes": culture_entry.get("respect_notes", []),
                "avoid_assumptions": culture_entry.get("avoid_assumptions", []),
            }

    return result
