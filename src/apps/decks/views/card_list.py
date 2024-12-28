from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.list import ListView

from ..models import Card
from .utils.auth import get_creator_deck
from .utils.context import set_card_context_headings


class CardListView(LoginRequiredMixin, ListView):
    model = Card

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        self.deck = get_creator_deck(request.user, kwargs.get("deck_id"))
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
        set_card_context_headings(context, "cards")
        return context
