from django.shortcuts import render

# ───────────────────────────────────────────────────────────────
# View: CEENI Civic Documents List
# Path: /ceeni-documents/
# Template: landing/docs_list.html
# ───────────────────────────────────────────────────────────────

def docs_list_view(request):
    """
    Public-facing view to show a list of CEENI civic documents,
    including the Bill, guides, historical background, narratives, and Constitution.

    Renders a responsive grid of cards using:
        - landing/partials/_docs_list_grid.html

    Template:
        landing/docs_list.html
    """
    return render(request, 'landing/docs_list.html')
