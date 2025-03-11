from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..forms import DeckForm
from ..models import Deck
from .utils.auth import get_creator_deck
from .utils.context import set_context_headings, set_prefixed_deck_context_headings


class DeckCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Deck
    form_class = DeckForm
    success_message = "Deck '%(title)s' created successfully"

    def get_success_url(self):
        return reverse("decks:card_list", kwargs={"deck_id": self.object.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        # Save model
        response = super().form_valid(form)
        # Collect saved model
        self.object.users.add(self.request.user)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_context_headings(context, "Create Metadata - New Deck")
        context["is_create_view"] = True
        return context


class DeckUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Deck
    form_class = DeckForm
    success_message = "Deck '%(title)s' updated successfully"
    pk_url_kwarg = "deck_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        get_creator_deck(request.user, kwargs.get("deck_id"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_prefixed_deck_context_headings(context, "Update Metadata")
        return context


class DeckDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Deck
    success_message = "Deck '%(title)s' deleted successfully"
    pk_url_kwarg = "deck_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        get_creator_deck(request.user, kwargs.get("deck_id"))

        return super().dispatch(request, *args, **kwargs)

    def get_success_message(self, _):
        return self.success_message % {"title": self.object.title}

    def get_success_url(self):
        return reverse("decks:deck_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_context_headings(context, f"Delete Deck '{context["deck"].title}'")
        return context
