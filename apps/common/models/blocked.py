from django.db import models
from django.conf import settings
from django.utils import timezone


class BlockedNickname(models.Model):
    """
    Stores forbidden words or nicknames with audit trail.
    Used across CEENI for nickname filtering, comment moderation, etc.
    """

    word = models.CharField(
        max_length=64,
        unique=True,
        help_text="Blocked word or nickname (e.g. slurs, political or ethnic insults)"
    )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blocked_nicknames_added",
        help_text="User who first added this term"
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blocked_nicknames_modified",
        help_text="User who last modified this term"
    )

    class Meta:
        verbose_name = "Blocked Nickname"
        verbose_name_plural = "Blocked Nicknames"
        ordering = ["word"]

    def __str__(self):
        return self.word
