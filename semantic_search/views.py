from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from .services.embeddings import embed_text, model_name
from .services.ranker import cosine_top_k


def _event_text(e: Event) -> str:
    parts = [
        e.title or "",
        e.description or "",
        e.category or "",
        e.tags or "",
    ]
    return " | ".join([p.strip() for p in parts if p and p.strip()])


def semantic_search(request):
    q = (request.GET.get("q") or "").strip()
    only_future = request.GET.get("future", "0") == "0"

    results = []
    if q:
        try:
            q_vec = embed_text(q)
        except RuntimeError as exc:
            messages.error(request, str(exc))
            q_vec = []

        qs = Event.objects.all()
        if only_future:
            qs = qs.filter(scheduled_for__gte=timezone.now())

        items = []
        for e in qs:
            items.append((e, getattr(e, "embedding", None)))

        ranked = cosine_top_k(q_vec, items, k=20)
        results = ranked

    context = {
        "query": q,
        "results": results,
        "only_future": only_future,
        "embedding_model": model_name(),
    }
    return render(request, "semantic_search/search.html", context)
