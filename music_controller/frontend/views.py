from django.shortcuts import render

# Render index template and let react take care of it
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')