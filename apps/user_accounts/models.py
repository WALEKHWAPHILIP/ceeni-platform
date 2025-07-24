import phonenumbers
from nanoid import generate

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


# ---------------------------------------------------------------------
# VALIDATOR: Ensure phone number is in E.164 format (e.g., +254712345678)
# ---------------------------------------------------------------------
from apps.common.validators.identity import validate_phone_e164  # Shared validator)


# ---------------------------------------------------------------------
# VALIDATOR: Enforce clean, safe, and culturally appropriate nicknames
# ---------------------------------------------------------------------
from apps.common.validators.identity import validate_nickname






# ---------------------------------------------------------------------
# CONSTANTS: For username suffix generation
# ---------------------------------------------------------------------
CUSTOM_NANO_ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'  # Lowercase letters + digits
CUSTOM_NANO_SIZE = 6                                            # Length of NanoID suffix



# ---------------------------------------------------------------------
# CUSTOM USER MANAGER: Handles creation of regular and superusers
# ---------------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, nickname=None, **extra_fields):
        """
        Create and save a CustomUser with the given phone number, nickname, and password.
        """
        if not phone_number:
            raise ValueError("Phone number is required.")
        if not nickname:
            raise ValueError("Nickname is required.")

        validate_phone_e164(phone_number)

        user = self.model(
            phone_number=phone_number,
            nickname=nickname,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, nickname="admin", **extra_fields):
        """
        Create and save a superuser with elevated privileges.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, nickname, **extra_fields)

# ---------------------------------------------------------------------
# CUSTOM USER MODEL: Auth via phone number, unique auto-generated username
# ---------------------------------------------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_phone_e164],
        help_text="Phone number in E.164 format (e.g., +254712345678)"
    )
    username = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        help_text="Auto-generated username based on nickname + NanoID"
    )
    nickname = models.CharField(
        max_length=20,
        validators=[validate_nickname],
        help_text="Nickname must be 3–10 characters. Letters, numbers, underscores only."
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return f"{self.nickname} ({self.phone_number})"

    def generate_username(self):
        """
        Generate a unique username using:
        - Normalized nickname (lowercased, max 10 chars, underscores for spaces)
        - Suffix from lowercase a–z0–9 NanoID (length = 6)
        Total username length is capped at 32 characters.
        """
        base = self.nickname.strip().lower().replace(" ", "-")[:10]
        suffix = generate(CUSTOM_NANO_ALPHABET, CUSTOM_NANO_SIZE)
        return f"{base}-{suffix}"

    def save(self, *args, **kwargs):    
        """
        On save:
        - Convert nickname to uppercase before saving.
        - If no username is set, generate one from nickname + NanoID.
        - Use a safe loop to avoid username collisions.
        """
        if self.nickname:
            self.nickname = self.nickname.upper()  # Enforce capital letters

        if not self.username and self.nickname:
            max_attempts = 10  # Avoid infinite loops on rare collisions
            for _ in range(max_attempts):
                candidate = self.generate_username()
                if not CustomUser.objects.filter(username=candidate).exists():
                    self.username = candidate
                    break
            else:
                raise ValueError("Could not generate a unique username after 10 attempts.")
        super().save(*args, **kwargs)
