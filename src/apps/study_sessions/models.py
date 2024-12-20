from django.conf import settings
from django.db import models
from django.forms import ValidationError

from ..decks.models import Card, Deck


class StudySession(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="study_sessions",
    )
    deck = models.ForeignKey(
        Deck, null=True, on_delete=models.SET_NULL, related_name="study_sessions"
    )
    create_date = models.DateField(auto_now_add=True)


class Response(models.Model):
    study_session = models.ForeignKey(
        StudySession, on_delete=models.CASCADE, related_name="responses"
    )
    card = models.ForeignKey(
        Card, null=True, on_delete=models.SET_NULL, related_name="responses"
    )
    is_correct = models.BooleanField()

    def clean(self):
        super().clean()

        if (
            self.card
            and self.study_session
            and self.card.deck != self.study_session.deck
        ):
            raise ValidationError("Card deck must match study session deck.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
