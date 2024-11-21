from django.shortcuts import render


def index(request):
    return render(request, "nonoverrides/index.html", {"head_title": "FlashMode"})
