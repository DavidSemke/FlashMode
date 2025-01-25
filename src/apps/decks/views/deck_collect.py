from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View

from ...decks.models import Deck

User = get_user_model()


class DeckCollectView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(
            Deck.objects.select_related("creator").annotate(
                is_collected=Exists(
                    Deck.objects.filter(id=OuterRef("pk"), users=self.request.user.id)
                )
            ),
            id=kwargs.get("deck_id"),
        )

        if deck.private and request.user.id != deck.creator.id:
            raise PermissionDenied()

        if deck.is_collected:
            deck.users.remove(User.objects.get(id=request.user.id))
        else:
            deck.users.add(User.objects.get(id=request.user.id))

        return redirect(reverse("decks:deck_detail", kwargs={"deck_id": deck.id}))
