from django.core.exceptions import PermissionDenied
from django.db.models import (
    Count,
    DateField,
    ExpressionWrapper,
    F,
    FloatField,
    IntegerField,
    OuterRef,
    Subquery,
)
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.detail import DetailView

from ...study_sessions.models import Response, StudySession
from ..models import Deck


class DeckDetailView(DetailView):
    model = Deck
    pk_url_kwarg = "deck_id"

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(
            Deck.objects.select_related("creator"), id=kwargs.get("deck_id")
        )

        if deck.private and deck.creator.id != request.user.id:
            raise PermissionDenied()

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("creator")
            .annotate(card_count=Count("cards"))
        )

        if self.request.user.is_authenticated:
            last_played_query = (
                StudySession.objects.filter(
                    student__id=self.request.user.id, deck__id=OuterRef("pk")
                )
                .order_by("-create_date")
                .values("create_date")[:1]
            )
            queryset = queryset.annotate(
                last_played=Subquery(last_played_query, output_field=DateField())
            )

            cards_completed_query = (
                Response.objects.filter(
                    is_correct__isnull=False,
                    study_session__deck=OuterRef("pk"),
                    study_session__create_date__gte=(
                        timezone.now() - timezone.timedelta(days=7)
                    ),
                )
                .values("study_session__deck")
                .annotate(count=Count("id"))
                .values("count")
            )
            queryset = queryset.annotate(
                cards_completed=Subquery(
                    cards_completed_query, output_field=IntegerField()
                )
            )

            cards_completed_correctly_query = (
                Response.objects.filter(
                    is_correct=True,
                    study_session__deck__id=self.kwargs["deck_id"],
                    study_session__create_date__gte=(
                        timezone.now() - timezone.timedelta(days=7)
                    ),
                )
                .values("study_session__deck")
                .annotate(count=Count("id"))
                .values("count")
            )

            queryset = queryset.annotate(
                cards_completed_correctly=Subquery(
                    cards_completed_correctly_query, output_field=IntegerField()
                )
            )

            queryset = queryset.annotate(
                accuracy=ExpressionWrapper(
                    F("cards_completed_correctly") * 100.0 / F("cards_completed"),
                    output_field=FloatField(),
                )
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.object
        context["main_h1"] = f"Deck '{deck.title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
