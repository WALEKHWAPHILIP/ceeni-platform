import os
from typing import List
import numpy as np

# Embedding vector size (dimension).
# Default is 1536 for OpenAI's 'text-embedding-3-small',
# but can be overridden with the CEENI_EMBED_DIM environment variable.
EMBED_DIM = int(os.getenv("CEENI_EMBED_DIM", 1536))

# Default embedding model name; configurable via environment variable.
MODEL_NAME = os.getenv("CEENI_EMBED_MODEL", "text-embedding-3-small")


def embed_texts(texts: List[str]) -> List[np.ndarray]:
    """
    Generate embeddings (vector representations) for a list of input texts.

    Supports multiple providers:
      1. "stub" (default) — Generates random vectors with a fixed RNG seed.
         Useful for development, testing, or offline environments.
      2. "openai" — Uses OpenAI's Embedding API.

    Provider selection is controlled by the CEENI_EMBED_PROVIDER environment variable.

    Args:
        texts (List[str]): List of input strings to embed.

    Returns:
        List[np.ndarray]: List of NumPy arrays (dtype=float32), each of size EMBED_DIM.

    Environment Variables:
        CEENI_EMBED_PROVIDER: "stub" (default) or "openai"
        CEENI_EMBED_DIM: embedding vector dimension (default 1536)
        CEENI_EMBED_MODEL: model name (default "text-embedding-3-small")
    """
    provider = os.getenv("CEENI_EMBED_PROVIDER", "stub").lower()

    if provider == "stub":
        # Stub mode: deterministic random embeddings for reproducibility
        rng = np.random.default_rng(42)  # fixed seed for consistent runs
        return [rng.normal(size=EMBED_DIM).astype("float32") for _ in texts]

    if provider == "openai":
        # OpenAI mode: call the Embeddings API
        from openai import OpenAI
        client = OpenAI()

        # Create embeddings for all texts in a single batch request
        res = client.embeddings.create(model=MODEL_NAME, input=texts)

        # Convert each embedding from list[float] to NumPy array
        return [np.asarray(d.embedding, dtype="float32") for d in res.data]

    # Any unknown provider results in a hard error
    raise RuntimeError(f"Unknown CEENI_EMBED_PROVIDER={provider}")


# Public API for this module
__all__ = ["embed_texts", "MODEL_NAME", "EMBED_DIM"]
