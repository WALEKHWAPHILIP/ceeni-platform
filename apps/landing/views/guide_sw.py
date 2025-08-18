from django.shortcuts import render

def friendly_guide_sw_view(request):
    # Ramani ya haraka kwa sehemu 7 za Mwongozo wa Kirafiki (Kiswahili)
    guide_sw_quick_nav = [
        {"id": "section-1", "label": "1. Utangulizi"},
        {"id": "section-2", "label": "2. Tatizo"},
        {"id": "section-3", "label": "3. Muswada Unafanya Nini"},
        {"id": "section-4", "label": "4. Inavyofanya Kazi"},
        {"id": "section-5", "label": "5. Kwa Nini Ni Faida kwa Wote"},
        {"id": "section-6", "label": "6. Unaweza Kufanya Nini"},
        {"id": "section-7", "label": "7. Wito wa Mwisho"},
    ]

    # Onyesha template ya mwongozo wa kirafiki (Kiswahili) na ramani ya haraka
    return render(
        request,
        "landing/ceeni_content/guide_sw/friendly_guide_sw.html",
        {"guide_sw_quick_nav": guide_sw_quick_nav}
    )
