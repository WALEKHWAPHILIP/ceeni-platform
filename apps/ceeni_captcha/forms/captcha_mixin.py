# apps/ceeni_captcha/forms/captcha_mixin.py

import random

from django import forms
from django.core.exceptions import ValidationError

# Import all supported Captcha models
# These represent different types of civic and jumbled knowledge questions.
from apps.ceeni_captcha.models import (
    CivicCaptcha,
    JumbledLeaderCaptcha,
    JumbledWardCaptcha,
    JumbledConstituencyCaptcha,
    JumbledCountyCaptcha,
    PoliticalPartyLeaderCaptcha,
)

# Default whitelist of models to draw captchas from
# Can be overridden by a custom whitelist passed to the form/mixin.
DEFAULT_CAPTCHA_MODELS = [
    CivicCaptcha,
    JumbledLeaderCaptcha,
    JumbledWardCaptcha,
    JumbledConstituencyCaptcha,
    JumbledCountyCaptcha,
    PoliticalPartyLeaderCaptcha,
]




class CaptchaFieldMixin(forms.Form):
    """
    CaptchaFieldMixin
    
    A reusable Django form mixin that injects a civic/jumbled captcha challenge into any form.

    Features:
    - Supports randomized selection from multiple models
    - Prevents repetition using session-based tracking
    - Allows difficulty range control
    - Fully backend-validated for security
    """

    # Captcha ID used to fetch the model instance on form submission (hidden)
    captcha_slug = forms.CharField(widget=forms.HiddenInput())

    # Captcha response field shown to the user
    captcha_response = forms.CharField(
        label="Captcha Challenge",
        help_text="→",
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Type your answer (cAse iNSeNSiTiVe) here..."
        })
    )

    def __init__(
        self,
        *args,
        request=None,
        difficulty_range=(0, 3),
        model_whitelist=None,
        **kwargs
    ):
        """
        Initializes the captcha challenge on form load.

        Accepts:
        - request: Django HttpRequest, used to track captcha models seen in session
        - difficulty_range: Tuple of min/max difficulty for filtering
        - model_whitelist: Optional list of captcha model classes to restrict selection
        """
        self.request = request
        super().__init__(*args, **kwargs)

        # Track used captcha model types in session to avoid repetition
        used_labels = self.request.session.get("used_captcha_models", []) if self.request else []

        # Use custom whitelist if provided, otherwise fallback to default models
        available_models = model_whitelist or DEFAULT_CAPTCHA_MODELS

        # Filter out captcha models already used by the user in this session
        unused_models = [
            model for model in available_models
            if model._meta.model_name not in used_labels
        ]

        # Fallback: if all have been used, reset session and reuse all models
        if not unused_models:
            unused_models = available_models
            if self.request:
                self.request.session["used_captcha_models"] = []

        # Gather eligible questions from selected models based on difficulty
        eligible_questions = []
        for model_cls in unused_models:
            qs = model_cls.objects.filter(active=True, difficulty__range=difficulty_range)
            eligible_questions += list(qs)

        # Graceful handling if no captchas are available
        if not eligible_questions:
            self.fields["captcha_slug"].initial = ''
            self.fields["captcha_response"].label = 'Captcha unavailable'
            self.fields["captcha_response"].help_text = 'No available captcha questions at this time.'
            return

        # Randomly select one captcha instance
        instance = random.choice(eligible_questions)
        self._current_captcha = instance

        # Populate form fields with selected captcha details
        self.fields["captcha_slug"].initial = instance.slug
        self.fields["captcha_response"].label = instance.question_text

        # Optionally show hint if available
        if instance.hint:
            self.fields["captcha_response"].help_text += f" Hint: {instance.hint}"

        # Log the model as used for this session
        if self.request:
            model_name = instance.__class__._meta.model_name
            if model_name not in used_labels:
                used_labels.append(model_name)
                self.request.session["used_captcha_models"] = used_labels

    def clean(self):
        """
        Validates that the user's response matches the correct answer stored in the DB.

        Ensures:
        - Captcha still exists and is active
        - Answer matches (case- and whitespace-insensitive)
        - Secure fallback if model is missing
        """
        cleaned_data = super().clean()
        slug = cleaned_data.get("captcha_slug")
        response = cleaned_data.get("captcha_response")

        if not slug or not response:
            raise ValidationError("Captcha question or response missing.")

        # Search through all known captcha models to find matching slug
        for model in DEFAULT_CAPTCHA_MODELS:
            try:
                obj = model.objects.get(slug=slug, active=True)
                if obj.correct_answer.strip().lower() != response.strip().lower():
                    raise ValidationError("Incorrect captcha answer. Try again.")
                break
            except model.DoesNotExist:
                continue
        else:
            # If no model matched, assume stale or tampered captcha
            raise ValidationError("This captcha is no longer valid. Please reload the page.")

        return cleaned_data
