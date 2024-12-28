from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from ...models import Deck


def get_creator_deck(request_user, deck_id):
    deck = get_object_or_404(Deck.objects.select_related("creator"), id=deck_id)

    if deck.creator.id != request_user.id:
        raise PermissionDenied()

    return deck
