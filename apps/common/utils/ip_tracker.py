# ────────────────────────────────────────────────────────────────
# FILE: apps/common/utils/ip_tracker.py
# PURPOSE: IP address detection utility – proxy aware
# ────────────────────────────────────────────────────────────────

def get_client_ip(request):
    """
    Returns the real IP address of the client, accounting for proxies.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Can contain multiple IPs – client, proxy1, proxy2, ...
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip
