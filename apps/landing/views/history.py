from django.shortcuts import render


def bill_history_view(request):
    # Define the quick navigation items for the bill history page
    # Each dict contains:
    #   - "id": Matches the HTML anchor ID for the target section in the page
    #   - "label": The clickable text displayed in the navigation menu
    history_quick_nav = [
        {"id": "section-1", "label": "1. Introduction"},
        {"id": "section-2", "label": "2. Historical Context"},
        {"id": "section-3", "label": "3. Tribalism in Governance"},
        {"id": "section-4", "label": "4. Institutional Impact"},
        {"id": "section-5", "label": "5. Legal Gaps"},
        {"id": "section-6", "label": "6. Rationale for the Bill"},
        {"id": "section-7", "label": "7. Conclusion"},
    ]
    
    # Render the "bill_history.html" template with the navigation data
    # Passes 'history_quick_nav' to be used in the template for generating jump links
    return render(
        request,
        "landing/ceeni_content/bill_history/bill_history.html",
        {"history_quick_nav": history_quick_nav}
    )
