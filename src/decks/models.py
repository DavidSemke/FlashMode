from django.conf import settings
from django.db import models


class Deck(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="decks_in_use"
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="decks_created"
    )
    create_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    private = models.BooleanField(default=False)


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards")
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)
