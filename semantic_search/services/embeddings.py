import threading

_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
_lock = threading.Lock()
_model = None


def get_model():
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                try:
                    from sentence_transformers import SentenceTransformer
                except Exception as exc:
                    raise RuntimeError(
                        "Could not load sentence-transformers. "
                        "Check transformers/huggingface-hub versions in this environment."
                    ) from exc
                _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_text(text: str) -> list[float]:
    text = (text or "").strip()
    if not text:
        return []
    model = get_model()
    vec = model.encode([text], normalize_embeddings=True)[0]
    return vec.tolist()


def model_name() -> str:
    return _MODEL_NAME
