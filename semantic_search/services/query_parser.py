from __future__ import annotations


def parse_query(text: str) -> dict:
    """
    Optional helper to extract simple filters from a natural query.
    Currently returns the raw query only.
    """
    return {"query": (text or "").strip(), "filters": {}}
