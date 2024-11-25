from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Deck


class DeckListView(ListView):
    model = Deck
    paginate_by = 20

    def get(self, request):
        return render(request, "decks/deck_list.html", {"head_title": "FlashMode"})


class DeckDetailView(DetailView):
    model = Deck

    def get(self, request):
        return render(request, "decks/deck_detail.html", {"head_title": "FlashMode"})
