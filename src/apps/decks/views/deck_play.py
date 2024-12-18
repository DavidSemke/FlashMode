from django.urls import reverse
from django.views.generic import RedirectView

from ...study_sessions.models import StudySession


class DeckPlayView(RedirectView):
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     try:
        #         self.study_session = StudySession.objects.create(
        #             student=request.user, deck=kwargs.get("deck_id")
        #         )
        #     except:
        #         pass

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if self.study_session:
            return reverse(
                "decks:study_session",
                kwargs={**kwargs, "study_session_id": self.study_session.id},
            )
        else:
            return reverse("decks:study_session_guest", kwargs)
