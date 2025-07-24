from django.shortcuts import render

# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/landing/views.py
# PURPOSE:
#   - Defines views for the public-facing CEENI landing page.
#   - Provides an entry point for civic engagement and motivational content.
# ───────────────────────────────────────────────────────────────────────────────

def index(request):
    """
    Public Homepage View (Landing Page)

    Handles HTTP GET requests to the root URL (`/`) and renders the 
    main landing page template. This view serves as the public-facing 
    entry point to the CEENI platform, designed to display civic content, 
    motivation, and general platform introduction.

    Template:
        landing/index.html

    Context:
        None (static for now; dynamic content can be added later)

    Returns:
        HttpResponse with rendered landing page template.
    """
    return render(request, 'landing/index.html')
