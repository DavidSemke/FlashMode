from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from ...models import Deck


def get_creator_deck(creator, deck_id):
    deck = get_object_or_404(Deck.objects.select_related("creator"), id=deck_id)

    if deck.creator.id != creator.id:
        raise PermissionDenied()

    return deck
