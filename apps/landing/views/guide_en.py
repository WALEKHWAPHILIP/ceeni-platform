from django.shortcuts import render


def friendly_guide_en_view(request):
    # Define the quick navigation items for the Friendly Guide page
    # Each dict contains:
    #   - "id": Matches the HTML anchor ID for the target section in the page
    #   - "label": The clickable text displayed in the navigation menu
    guide_en_quick_nav = [
        {"id": "section-1", "label": "1. Introduction"},
        {"id": "section-2", "label": "2. The Problem"},
        {"id": "section-3", "label": "3. What the Bill Does"},
        {"id": "section-4", "label": "4. How It Works"},
        {"id": "section-5", "label": "5. Why It’s Good for Everyone"},
        {"id": "section-6", "label": "6. What You Can Do"},
        {"id": "section-7", "label": "7. Closing Call"},
    ]

    # Render the "friendly_guide_en.html" template with the navigation data
    # Passes 'guide_en_quick_nav' to be used in the template for generating jump links
    return render(
        request,
        "landing/ceeni_content/guide_en/friendly_guide_en.html",
        {"guide_en_quick_nav": guide_en_quick_nav}
    )
