from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

from ..models import Card, Deck


class CardListView(LoginRequiredMixin, ListView):
    model = Card

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, id=kwargs.get("deck_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(deck=self.deck.id)
            .select_related("deck")
            .order_by("question")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        context["main_h1"] = f"Cards - Deck '{context["deck"].title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
