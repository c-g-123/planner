from django.shortcuts import render

TEMPLATE_PATH = "core/index.html"

def index(request):
    return render(request, TEMPLATE_PATH)
