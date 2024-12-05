from datetime import timedelta

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
from django.utils import timezone
from django.views.generic.detail import DetailView

from ...study_sessions.models import Response, StudySession
from ..models import Deck


class DeckDetailView(DetailView):
    model = Deck

    # use get to get one object instead of filter !!!

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("creator")
            .annotate(card_count=Count("cards"))
            .filter(pk=self.kwargs["pk"])
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
                    study_session__deck=OuterRef("pk"),
                    study_session__create_date__gte=timezone.now().date()
                    - timedelta(days=7),
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
                    study_session__deck__id=self.kwargs["pk"],
                    study_session__create_date__gte=timezone.now().date()
                    - timedelta(days=7),
                    is_correct=True,
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
                    F("cards_completed_correctly") * 1.0 / F("cards_completed"),
                    output_field=FloatField(),
                )
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck: Deck = self.get_object()
        context["head_title"] = deck.title + " - FlashMode"
        return context
