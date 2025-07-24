import phonenumbers
import re
from django.core.exceptions import ValidationError
from apps.common.models import BlockedNickname  # Model-based profanity filtering

def validate_phone_e164(value):
    """
    Validate that a phone number is in E.164 format (e.g., +254712345678).
    """
    try:
        parsed = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed):
            raise ValidationError("Invalid phone number format.")
    except phonenumbers.NumberParseException:
        raise ValidationError("Invalid phone number. Use format like +254712345678.")






def contains_profanity(value):
    """
    Checks if the input value contains any blocked word (case-insensitive).
    Normalizes spacing and punctuation before checking.
    """
    nickname = value.lower().strip().replace("_", " ").replace("-", " ")
    words = nickname.split()

    for word in words:
        if BlockedNickname.objects.filter(word__iexact=word).exists():
            return True
    return False


def validate_nickname(value):
    """
    Validates nickname input from the user.
    - Must be 3–10 characters
    - Can contain letters, numbers, spaces, or underscores
    - No known profane or blocked terms
    """
    if not (3 <= len(value) <= 10):
        raise ValidationError("Nickname must be between 3 and 10 characters.")

    if not re.match(r'^[a-zA-Z0-9 _-]+$', value):
        raise ValidationError("Nickname can only contain letters, numbers, spaces, hyphens, or underscores.")

    if contains_profanity(value):
        raise ValidationError("Please choose a different nickname — this word is not allowed.")
