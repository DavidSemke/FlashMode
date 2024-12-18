from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ..models import Card, Deck


class StudySessionGuestView(TemplateView):
    template_name = "study_session"

    def get(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck.objects.get(pk=kwargs.get("deck_id")))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        context["main_h1"] = f"Study Session - Deck '{context["deck"].title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
