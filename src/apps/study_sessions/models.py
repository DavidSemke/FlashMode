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
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["study_session", "card"], name="unique_study_session_card"
            ),
            models.UniqueConstraint(
                fields=["study_session", "position"],
                name="unique_study_session_position",
            ),
        ]

    study_session = models.ForeignKey(
        StudySession, on_delete=models.CASCADE, related_name="responses"
    )
    card = models.ForeignKey(
        Card, null=True, on_delete=models.SET_NULL, related_name="responses"
    )
    # A response is created for each card on study session create
    # This is because position (for card order) is required
    # Responses to cards not yet completed have is_correct = null
    is_correct = models.BooleanField(null=True, default=None)
    # Every study session has a random card order
    # Response position = card position in that order
    position = models.SmallIntegerField()

    def clean(self):
        super().clean()

        # self.card might be None
        if self.card and self.card.deck != self.study_session.deck:
            raise ValidationError("Card deck must match study session deck.")

        if self.is_correct is None:
            later_responses = Response.objects.filter(
                study_session=self.study_session,
                position__gt=self.position,
                is_correct__isnull=False,
            )

            if later_responses.exists():
                raise ValidationError(
                    "If 'is_correct' is null, all subsequent responses in the same"
                    + " study session must also have 'is_correct' as null."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
