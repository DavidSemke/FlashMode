from django.conf import settings
from django.db import models
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
    title = models.CharField(max_length=50, blank=True)
    private = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("deck_detail", kwargs={"pk": self.pk})


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards")
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)
