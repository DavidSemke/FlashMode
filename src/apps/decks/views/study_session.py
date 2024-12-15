from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ..models import Deck, StudySession


class StudySessionView(TemplateView):
    template_name = "study_session"

    def get(self, request, *args, **kwargs):
        ss_id = kwargs.get("study_session_id")

        if request.user.is_authenticated and ss_id:
            self.study_session = get_object_or_404(
                (
                    StudySession.objects.select_related("deck").prefetch_related(
                        "deck__cards"
                    )
                ),
                id=ss_id,
            )

            if self.study_session.student != request.user.id:
                raise PermissionDenied("User id does not match student id")

            self.deck = self.study_session.deck
        else:
            self.deck = get_object_or_404(Deck.objects.get(pk=kwargs.get("deck_id")))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck"] = self.deck
        context["main_h1"] = f"Study Session - Deck '{context["deck"].title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
