from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ..models import Deck


class StudySessionGuestView(TemplateView):
    template_name = "decks/study_session_guest.html"

    def get(self, request, *args, **kwargs):
        self.deck = get_object_or_404(
            Deck.objects.prefetch_related("cards"), id=kwargs.get("deck_id")
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_list"] = list(self.deck.cards.values())
        context["card_count"] = len(context["card_list"])
        context["main_h1"] = f"Study Session - Deck '{context["deck"].title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
