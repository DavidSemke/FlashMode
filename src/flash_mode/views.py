from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


def index(request):
    return render(request, "nonoverrides/index.html")
