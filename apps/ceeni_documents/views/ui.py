# apps/ceeni_documents/views/ui.py

from django.views.decorators.http import require_GET
from django.shortcuts import render

from apps.ceeni_documents.services.embedder import embed_texts
from apps.ceeni_documents.services.search import knn_search

MAX_K = 20  # Defensive cap on max number of search results to prevent performance degradation and abuse

@require_GET
def search_htmx(request):
    """
    Handles HTMX-enhanced GET requests for document semantic search.
    This endpoint accepts a query parameter 'q' (user search text) and optional 'k' (number of results).

    Workflow:
    1. Extract and sanitize input parameters from query string.
       - 'q': search query string, whitespace-trimmed.
       - 'k': number of top results requested, validated and bounded by MAX_K.
    2. If 'q' is non-empty, embed the query text into vector space using pre-trained embedder.
    3. Perform k-Nearest Neighbor (k-NN) search over section embeddings to find semantically closest sections.
    4. Construct a simplified results payload including score, document metadata, and a snippet of section text.
    5. Render partial HTML response with the search results injected, to be swapped dynamically via HTMX.

    Design considerations:
    - HTMX is used for partial page updates, improving UI responsiveness without full reload.
    - Defensive programming applied on 'k' parameter to prevent unreasonable large queries.
    - Embeddings and search are asynchronous-friendly but handled synchronously here for simplicity.
    - Only top-k results are returned with snippet length limited to 400 characters for UI consistency.
    - This view abstracts vector search logic behind service layers for modularity and maintainability.

    Args:
        request (HttpRequest): The incoming HTTP GET request with query parameters.

    Returns:
        HttpResponse: Rendered partial template '_search_results.html' with context containing search results,
                      original query, and number of results requested.
    """

    # Extract and sanitize the search query from request GET parameters
    q = (request.GET.get("q") or "").strip()

    # Defensive handling of 'k' parameter: default to 5, fallback on invalid input
    try:
        k = int(request.GET.get("k", 5))
    except ValueError:
        k = 5
    # Clamp k to between 1 and MAX_K to safeguard backend performance
    k = max(1, min(k, MAX_K))

    results = []
    if q:
        # Generate vector embedding for the query text (embedding model abstracted)
        vec = embed_texts([q])[0]

        # Perform vector similarity search to retrieve top-k relevant document sections
        knn = knn_search(vec, k)

        # Transform raw search results into structured data for template rendering
        for score, section in knn:
            doc = section.document
            results.append({
                "score": float(score),                      # similarity score (float) for relevance ranking
                "document_title": doc.title,                # title of the parent document
                "document_slug": doc.slug,                  # slug for URL construction or linking
                "doc_type": doc.doc_type,                    # document type/category metadata
                "section_index": section.index,             # section position within document for navigation
                "heading": section.heading,                  # section heading/title if available
                "snippet": (section.text or "")[:400],      # excerpt of section text for preview (max 400 chars)
            })

    # Render the partial HTML template with search results context
    # Intended for HTMX partial swap to dynamically update search results in UI without full reload
    return render(
        request,
        "ceeni_documents/partials/_search_results.html",
        {"results": results, "query": q, "k": k},
    )
