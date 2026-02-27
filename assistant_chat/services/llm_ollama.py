import requests
from django.conf import settings


def generate(prompt: str) -> str:
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": settings.OLLAMA_TEMPERATURE,
            "top_p": settings.OLLAMA_TOP_P,
            "num_ctx": settings.OLLAMA_NUM_CTX,
        },
    }

    try:
        response = requests.post(settings.OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(
            "No s'ha pogut connectar amb Ollama. Revisa que el servei estigui actiu."
        ) from exc
    except ValueError as exc:
        raise RuntimeError("Resposta invalida d'Ollama.") from exc

    return (data.get("response") or "").strip()
