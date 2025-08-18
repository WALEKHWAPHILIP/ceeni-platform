import numpy as np
from ..models import Section, Embedding


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute the cosine similarity between two vectors.

    Args:
        a (np.ndarray): First vector.
        b (np.ndarray): Second vector.

    Returns:
        float: Cosine similarity in the range [-1.0, 1.0].
               Higher values indicate greater similarity.

    Notes:
        - Adds a small epsilon (1e-9) to denominators to avoid division by zero.
        - Both `a` and `b` are expected to be 1D NumPy arrays of the same length.
    """
    na = np.linalg.norm(a) + 1e-9
    nb = np.linalg.norm(b) + 1e-9
    return float(np.dot(a, b) / (na * nb))


def knn_search(query_vec: np.ndarray, k: int = 5):
    """
    Perform a brute-force k-nearest neighbors search using cosine similarity.

    Args:
        query_vec (np.ndarray): Embedding vector for the query text.
        k (int): Number of top results to return (default: 5).

    Returns:
        List[Tuple[float, Section]]:
            - Cosine similarity score.
            - Corresponding `Section` object.

    Process:
        1. Retrieves all embeddings from the database.
        2. Computes cosine similarity between the query vector and each stored vector.
        3. Sorts results by similarity (highest first).
        4. Returns the top-k most similar sections.

    Implementation Details:
        - Uses `.select_related()` to fetch related Section and Document in one query,
          avoiding the N+1 query problem when accessing them later.
        - Uses `.iterator()` to reduce memory usage when scanning large datasets.
        - Embedding vectors are stored as raw bytes in the database; they are
          converted to NumPy float32 arrays using `np.frombuffer()`.
        - Currently uses brute-force linear search (O(N) complexity).
          For production-scale systems, replace with:
            * `pgvector` (Postgres vector extension)
            * FAISS (Facebook AI Similarity Search)
            * Annoy / HNSWlib (approximate nearest neighbor search)

    Example:
        >>> vec = np.random.rand(1536).astype("float32")
        >>> top_matches = knn_search(vec, k=3)
        >>> for score, section in top_matches:
        ...     print(score, section.title)
    """
    results = []

    # Fetch all embeddings with related Section and Document in one query
    qs = Embedding.objects.select_related("section", "section__document").all().iterator()

    for emb in qs:
        # Convert binary storage to NumPy array (float32)
        v = np.frombuffer(emb.vector, dtype="float32")

        # Compute similarity score
        score = _cosine(query_vec, v)

        # Store (score, section) pair
        results.append((score, emb.section))

    # Sort results by similarity score (highest first)
    results.sort(key=lambda x: x[0], reverse=True)

    # Return top-k matches
    return results[:k]
