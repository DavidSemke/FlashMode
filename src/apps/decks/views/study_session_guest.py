from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Deck


class StudySessionGuestView(TemplateView):
    template_name = "decks/study_session_guest.html"

    def get(self, request, *args, **kwargs):
        # If authenticated, study_session app should be used.
        # Redirect to deck play for setup, which in turn redirects
        # to proper destination.
        if request.user.is_authenticated:
            return redirect(reverse("decks:deck_play", kwargs={**kwargs}))

        self.deck = get_object_or_404(
            Deck.objects.prefetch_related("cards"), id=kwargs.get("deck_id")
        )

        if self.deck.private:
            raise PermissionDenied()

        self.card_list = list(self.deck.cards.values())
        self.card_count = len(self.card_list)

        if self.card_count == 0:
            return HttpResponse(
                content="All cards from this deck have been deleted.", status=422
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_list"] = self.card_list
        context["card_count"] = self.card_count
        context["main_h1"] = f"Study Session - Deck '{self.deck.title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
