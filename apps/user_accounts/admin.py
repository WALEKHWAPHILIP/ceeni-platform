# ------------------------------------------------------------------------------
# Django Admin Registration for CustomUser Model
# ------------------------------------------------------------------------------

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for the CustomUser model.
    Streamlined to use Django conventions while preserving CEENI custom behavior.
    """

    # ----------------------------------------------------------
    # Basic Config
    # ----------------------------------------------------------
    model = CustomUser

    # Fields shown in list view
    list_display = (
        "phone_number", "nickname", "username", "is_active", "is_staff"
    )
    list_filter = (
        "is_active", "is_staff", "is_superuser"
    )

    # ----------------------------------------------------------
    # Fields shown in detail/edit view
    # ----------------------------------------------------------
    fieldsets = (
        (None, {
            "fields": ("phone_number", "nickname", "password")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined")
        }),
        ("System", {
            "fields": ("username",)
        }),
    )

    readonly_fields = (
        "username", "last_login", "date_joined"
    )

    # ----------------------------------------------------------
    # Fields shown during user creation
    # ----------------------------------------------------------
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "nickname", "password1", "password2"),
        }),
    )

    # ----------------------------------------------------------
    # Search & Ordering
    # ----------------------------------------------------------
    search_fields = ("phone_number", "nickname")
    ordering = ("phone_number",)
