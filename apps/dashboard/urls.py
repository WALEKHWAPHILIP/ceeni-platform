# apps/dashboard/urls.py

from django.urls import path
from .views.home_view import home

app_name = 'dashboard'

urlpatterns = [
    path('', home, name='home'),
]
