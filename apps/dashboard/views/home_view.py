# apps/dashboard/views/home_view.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """
    Dashboard landing page after profile onboarding.
    """
    return render(request, 'dashboard/onboarding/index.html', {
        'user': request.user,
    })
