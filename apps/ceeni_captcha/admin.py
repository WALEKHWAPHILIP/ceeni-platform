# apps/ceeni_captcha/admin.py

"""
Admin registrations for CEENI Captcha models.

We deliberately use `admin.site.register(...)` instead of the `@admin.register(...)` decorator
because all captcha models share the same `BaseCaptchaAdmin` configuration. This promotes DRY 
code and avoids duplicating multiple admin subclasses that would otherwise do nothing.

If you later need model-specific admin behavior, consider subclassing `BaseCaptchaAdmin`
per model and switching to decorators.

See Django docs: https://docs.djangoproject.com/en/stable/ref/contrib/admin/#adminsite-register
"""

from django.contrib import admin
from .models import (
    CivicCaptcha,
    JumbledLeaderCaptcha,
    JumbledWardCaptcha,
    JumbledConstituencyCaptcha,
    JumbledCountyCaptcha,
    PoliticalPartyLeaderCaptcha,  # ✅ NEW
)


class BaseCaptchaAdmin(admin.ModelAdmin):
    """
    Shared admin configuration across all captcha types.
    """
    list_display = (
        "question_text",
        "correct_answer",
        "difficulty",
        "active",
        "updated_at",
    )
    list_filter = (
        "active",
        "difficulty",
        "tags",
    )
    search_fields = (
        "question_text",
        "correct_answer",
        "tags",
    )
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at", "slug")
    fieldsets = (
        (None, {
            "fields": (
                "question_text",
                "correct_answer",
                "hint",
                "explanation",
                "difficulty",
                "tags",
                "active",
                "slug",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# Register all concrete models using shared base admin
admin.site.register(CivicCaptcha, BaseCaptchaAdmin)
admin.site.register(JumbledLeaderCaptcha, BaseCaptchaAdmin)
admin.site.register(JumbledWardCaptcha, BaseCaptchaAdmin)
admin.site.register(JumbledConstituencyCaptcha, BaseCaptchaAdmin)
admin.site.register(JumbledCountyCaptcha, BaseCaptchaAdmin)
admin.site.register(PoliticalPartyLeaderCaptcha, BaseCaptchaAdmin)  # ✅ NEW
