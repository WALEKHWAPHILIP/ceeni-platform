from django.http import JsonResponse
from django.views.decorators.http import require_GET

from apps.ceeni_documents.services.embedder import embed_texts
from apps.ceeni_documents.services.search import knn_search

MAX_K = 20  # Maximum number of results to return, defensive cap to prevent abuse or overload

@require_GET
def search_api(request):
    """
    API endpoint to perform a semantic search over document sections.
    Accepts GET parameters:
        - q: the query text (string)
        - k: number of nearest neighbors to return (int, optional, default=5)
    Returns JSON with search results ranked by similarity score.
    """
    # Extract and sanitize the query parameter 'q'
    q = (request.GET.get("q") or "").strip()

    # Extract 'k' parameter, fallback to 5 if missing or invalid
    try:
        k = int(request.GET.get("k", 5))
    except ValueError:
        k = 5

    # Clamp 'k' to be within 1 and MAX_K to avoid excessive load
    k = max(1, min(k, MAX_K))

    # If query is empty, return empty results early
    if not q:
        return JsonResponse({"results": [], "query": q, "k": k})

    # Embed the query text into vector space using the embedder service
    vec = embed_texts([q])[0]

    # Perform K-Nearest Neighbor search to find the most relevant document sections
    results = knn_search(vec, k)

    # Prepare the payload of results with relevant metadata for the client
    payload = []
    for score, section in results:
        doc = section.document
        payload.append({
            "score": float(score),  # similarity score (float)
            "document_title": doc.title,
            "document_slug": doc.slug,
            "doc_type": doc.doc_type,
            "section_id": section.id,
            "section_index": section.index,
            "heading": section.heading,
            "snippet": (section.text or "")[:400],  # snippet: first 400 characters of section text
        })

    # Return JSON response with results and query metadata
    return JsonResponse({"results": payload, "query": q, "k": k})
