from django.shortcuts import render


def index(request):
    return render(request, "core/index.html", {"head_title": "FlashMode"})
