from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.urls import reverse


class Deck(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="decks_in_use"
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="decks_created",
    )
    create_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    private = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("decks:deck_detail", kwargs={"deck_id": self.pk})


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards")
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)


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
