from django.utils import timezone

from events.models import Event
from semantic_search.services.embeddings import embed_text
from semantic_search.services.ranker import cosine_top_k


def build_event_text(event: Event) -> str:
    return " | ".join(
        [
            (event.title or "").strip(),
            (event.description or "").strip(),
            (event.category or "").strip(),
            (event.tags or "").strip(),
        ]
    ).strip()


def retrieve_events(query: str, only_future: bool = True, k: int = 8, min_score: float = 0.25):
    query = (query or "").strip()
    if not query:
        return []

    try:
        q_vec = embed_text(query)
    except RuntimeError:
        return []

    qs = Event.objects.all()
    if only_future:
        qs = qs.filter(scheduled_for__gte=timezone.now())

    items = []
    for event in qs.only("id", "title", "scheduled_for", "category", "tags", "embedding"):
        emb = getattr(event, "embedding", None)
        if isinstance(emb, list) and emb:
            items.append((event, emb))

    ranked = cosine_top_k(q_vec, items, k=max(k, 20))
    ranked = [(event, score) for (event, score) in ranked if score >= min_score]
    return ranked[:k]
