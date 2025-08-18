from django.shortcuts import render

def index_view(request):
    """
    Public Homepage View (Landing Page)
    """
    return render(request, 'landing/index.html')
