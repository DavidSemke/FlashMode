from django.db.models import Count
from django.views.generic.list import ListView

from ..models import Deck


class DeckListView(ListView):
    model = Deck
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("creator")
            .annotate(card_count=Count("cards"))
            .order_by("-create_date")
        )

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_h1"] = "Decks"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context
