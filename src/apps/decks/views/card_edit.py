from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import CardForm
from ..models import Card, Deck


class CardCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Card
    form_class = CardForm
    success_message = "Card created successfully"
    pk_url_kwarg = "card_id"

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, id=kwargs.get("deck_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("decks:card_list", kwargs={"deck_id": self.deck.id})

    def form_valid(self, form):
        form.instance.deck = self.deck
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        set_context_headings(context, "create")
        return context


class CardUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Card
    form_class = CardForm
    success_message = "Card updated successfully"
    pk_url_kwarg = "card_id"

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, id=kwargs.get("deck_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("decks:card_list", kwargs={"deck_id": self.deck.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        set_context_headings(context, "update")
        return context


class CardDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Card
    success_message = "Card deleted successfully"
    pk_url_kwarg = "card_id"

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, id=kwargs.get("deck_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("decks:card_list", kwargs={"deck_id": self.deck.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        set_context_headings(context, "delete")
        return context


def set_context_headings(context, edit_type):
    context["main_h1"] = f"{edit_type.title()} Card - Deck '{context["deck"].title}'"
    context["head_title"] = f"{context["main_h1"]} - FlashMode"
