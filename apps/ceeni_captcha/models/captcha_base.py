# apps/ceeni_captcha/models/captcha_base.py

from django.db import models
from django.utils.text import slugify


class CaptchaBase(models.Model):
    """
    Abstract base model for all captcha types used in CEENI.
    Shared fields include question content, answer, difficulty, tags, and audit info.
    """

    question_text = models.TextField(
        help_text="Main question prompt (e.g., trivia, riddle, jumbled phrase)"
    )
    correct_answer = models.CharField(
        max_length=100,
        help_text="Expected correct answer (case-insensitive match)"
    )
    hint = models.TextField(
        blank=True,
        help_text="Optional hint to assist user in solving the captcha"
    )
    explanation = models.TextField(
        blank=True,
        help_text="Optional explanation shown after correct/incorrect answer (for civic learning)"
    )
    difficulty = models.IntegerField(
        default=1,
        help_text="Scale from 0 (very easy) to 5 (very hard)"
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords like 'elections,leadership,constitution'"
    )

    slug = models.SlugField(
        max_length=100,  # explicitly set length to a larger value
        unique=True,
        help_text="Unique slug for referencing or analytics"
    )
        
    active = models.BooleanField(
        default=True,
        help_text="Only active captchas will be used during registration or civic flow"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['active', 'difficulty']),
        ]

    def save(self, *args, **kwargs):
        # Auto-generate slug from question (if not already set)
        if not self.slug:
            self.slug = slugify(self.question_text[:80])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question_text[:60]}..."

    def get_model_label(self):
        """
        Returns a short, human-friendly name for the captcha source model.
        Used in the UI for transparency.
        """
        return self._meta.verbose_name.title()
