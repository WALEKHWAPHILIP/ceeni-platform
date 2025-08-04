# apps/common/context_processors/user_data.py
def global_user_data(request): 
    """
    Adds user and profile info to all templates if the user is authenticated.
    """
    if not request.user.is_authenticated:
        return {}

    # Get the related user profile if it exists
    profile = getattr(request.user, "userprofile", None)

    return {
        "ceeni_user": request.user,                             # Logged-in User object
        "ceeni_profile": profile,                                # Related profile (if any)
        "ceeni_photo": getattr(profile, "profile_image", None),  # Profile image (optional)
    }
