from django.shortcuts import render

def constitution_2010_view(request):
    return render(request, 'landing/ceeni_content/the_2010_constitution/the_2010_constitution.html')
