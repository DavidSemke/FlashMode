from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import CardForm
from ..models import Card
from .utils.auth import get_creator_deck
from .utils.context import set_card_edit_context_headings


class CardCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Card
    form_class = CardForm
    success_message = "Card created successfully"
    pk_url_kwarg = "card_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        self.deck = get_creator_deck(request.user, kwargs.get("deck_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("decks:card_list", kwargs={"deck_id": self.deck.id})

    def form_valid(self, form):
        form.instance.deck = self.deck
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        set_card_edit_context_headings(context, "create")
        return context


class CardUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Card
    form_class = CardForm
    success_message = "Card updated successfully"
    pk_url_kwarg = "card_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        self.deck = get_creator_deck(request.user, kwargs.get("deck_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("decks:card_list", kwargs={"deck_id": self.deck.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        set_card_edit_context_headings(context, "update")
        return context


class CardDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Card
    success_message = "Card deleted successfully"
    pk_url_kwarg = "card_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        self.deck = get_creator_deck(request.user, kwargs.get("deck_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("decks:card_list", kwargs={"deck_id": self.deck.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        set_card_edit_context_headings(context, "delete")
        return context
