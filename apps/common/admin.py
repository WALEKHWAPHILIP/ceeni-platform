# Register your models here.

from django.contrib import admin
from .models import BlockedNickname


@admin.register(BlockedNickname)
class BlockedNicknameAdmin(admin.ModelAdmin):
    list_display = ("word", "added_by", "modified_by", "added_at", "updated_at")
    search_fields = ("word",)
    readonly_fields = ("added_at", "updated_at", "added_by", "modified_by")
    list_filter = ("added_by", "modified_by")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user  # only set on creation
        obj.modified_by = request.user  # always update
        super().save_model(request, obj, form, change)
