from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Deck


class DeckListView(ListView):
    model = Deck
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("creator")
            .annotate(card_count=Count("cards"))
            .order_by("-create_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head_title"] = "Search Decks - FlashMode"
        return context


class DeckDetailView(DetailView):
    model = Deck

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck: Deck = self.get_object()
        context["head_title"] = deck.title + " - FlashMode"
        return context
