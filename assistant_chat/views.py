import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .services.llm_ollama import generate
from .services.prompts import build_prompt
from .services.retriever import retrieve_events


def chat_page(request):
    return render(request, "assistant_chat/chat.html")


def _parse_llm_json(raw_text: str):
    raw_text = (raw_text or "").strip()
    if not raw_text:
        raise ValueError("Empty response")

    if raw_text.startswith("```"):
        parts = [p for p in raw_text.split("```") if p.strip()]
        if parts:
            raw_text = parts[0].replace("json", "", 1).strip()

    return json.loads(raw_text)


@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    message = (payload.get("message") or "").strip()
    only_future = payload.get("only_future", True)
    if isinstance(only_future, str):
        only_future = only_future.lower() in {"1", "true", "yes", "on"}
    else:
        only_future = bool(only_future)

    if not message:
        return JsonResponse({"error": "Empty message"}, status=400)

    ranked = retrieve_events(message, only_future=only_future, k=8)

    candidates = []
    for event, score in ranked:
        candidates.append(
            {
                "id": int(event.pk),
                "title": event.title,
                "scheduled_date": event.scheduled_for.isoformat() if event.scheduled_for else None,
                "category": event.category,
                "tags": event.tags or "",
                "url": event.get_absolute_url(),
                "score": round(float(score), 3),
            }
        )

    llm_raw_output = ""
    if candidates:
        prompt = build_prompt(message, candidates)
        try:
            llm_raw_output = generate(prompt)
            llm_json = _parse_llm_json(llm_raw_output)
        except Exception:
            llm_json = {
                "answer": "T'he trobat alguns esdeveniments relacionats.",
                "recommended_ids": [c["id"] for c in candidates[:3]],
                "follow_up": "",
            }
    else:
        llm_json = {
            "answer": "Ara mateix no trobo cap esdeveniment que encaixi amb la teva peticio.",
            "recommended_ids": [],
            "follow_up": "Vols provar amb una altra categoria o ampliar les dates?",
        }

    allowed_ids = {c["id"] for c in candidates}
    recommended_ids = []
    for item in llm_json.get("recommended_ids", []):
        try:
            parsed_id = int(item)
        except (TypeError, ValueError):
            continue
        if parsed_id in allowed_ids:
            recommended_ids.append(parsed_id)

    cards = [c for c in candidates if c["id"] in recommended_ids]
    if not cards:
        cards = candidates[:3]

    response_payload = {
        "answer": llm_json.get("answer", ""),
        "follow_up": llm_json.get("follow_up", ""),
        "events": cards,
    }
    if settings.DEBUG:
        response_payload["raw_model_output"] = llm_raw_output

    return JsonResponse(response_payload)
