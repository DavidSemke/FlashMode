from random import shuffle

from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView

from ...decks.models import Card, Deck
from ...study_sessions.models import Response, StudySession


class DeckPlayView(RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            deck = get_object_or_404(
                Deck.objects.prefetch_related(
                    Prefetch("cards", queryset=Card.objects.only("id"))
                ),
                id=kwargs.get("deck_id"),
            )

            with transaction.atomic():
                self.study_session = StudySession.objects.create(
                    student=request.user, deck=deck
                )

                # deck.cards is a list of card ids
                card_list = list(deck.cards.all())
                shuffle(card_list)

                # Method bulk_create is not used because it skips
                # the save() method
                # The Response model uses save() for validation
                for pos, card in enumerate(card_list):
                    Response.objects.create(
                        study_session=self.study_session, card=card, position=pos
                    )

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        if hasattr(self, "study_session"):
            return reverse(
                "study_sessions:study_session",
                kwargs={"study_session_id": self.study_session.id},
            )
        else:
            return reverse("decks:study_session_guest", kwargs={**kwargs})
