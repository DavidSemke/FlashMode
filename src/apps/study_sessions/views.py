from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView

from ..decks.models import Card, Deck
from .models import StudySession


class StudySessionView(TemplateView):
    template_name = "study_session"

    def get(self, request, *args, **kwargs):
        ss_id = kwargs.get("study_session_id")

        if request.user.is_authenticated and ss_id:
            self.study_session = get_object_or_404(
                StudySession.objects.select_related("deck").prefetch_related(
                    "deck__cards"
                ),
                id=ss_id,
            )
            self.deck = self.study_session.deck

            if self.deck is None:
                raise Http404("No Deck matches the given query.")
            elif self.study_session.student != request.user.id:
                raise PermissionDenied("Study session was not created by current user")
            elif self.study_session.create_date <= timezone.now() - timedelta(hours=24):
                return HttpResponse(
                    content="This study session has expired", status=410
                )
            elif self.deck is None:
                return HttpResponse(
                    content="This study session has had its deck deleted", status=409
                )
            # else:
            #     card_id = self.study_session.card_order[self.study_session.position]
            #     card = Card.objects.get(id=card_id)

        else:
            self.deck = get_object_or_404(Deck.objects.get(pk=kwargs.get("deck_id")))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        context["main_h1"] = f"Study Session - Deck '{context["deck"].title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
