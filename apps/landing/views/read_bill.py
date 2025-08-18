from django.shortcuts import render


def read_the_bill_view(request):
    # Define the quick navigation items for the EEPR Bill page
    bill_quick_nav = [
        {"id": "section-1", "label": "1. Part I — Preliminary"},
        {"id": "section-2", "label": "2. Part II — Principles and Objectives"},
        {"id": "section-3", "label": "3. Part III — The Commission (CEENI)"},
        {"id": "section-4", "label": "4. Part IV — Data and Reporting Obligations"},
        {"id": "section-5", "label": "5. Part V — Complaints and Enforcement"},
        {"id": "section-6", "label": "6. Part VI — Public Participation"},
        {"id": "section-7", "label": "7. Part VII — Miscellaneous Provisions"},
        {"id": "section-8", "label": "8. First Schedule — Data Reporting Templates"},
        {"id": "section-9", "label": "9. Second Schedule — Equity Scorecard Metrics & Grading"},
        {"id": "section-10", "label": "10. Third Schedule — CEENI Tribunal Procedure"},
        {"id": "section-11", "label": "11. Fourth Schedule — Consequential Amendments"},
        {"id": "section-12", "label": "12. Fifth Schedule — Representation Allocation Formula"},
    ]

    return render(
        request,
        "landing/ceeni_content/bill_eepr_2025/read_the_bill.html",
        {"bill_quick_nav": bill_quick_nav}
    )
