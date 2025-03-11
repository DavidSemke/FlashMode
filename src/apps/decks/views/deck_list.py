from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.views.generic.list import ListView

from ..models import Deck
from .utils.context import set_context_headings


class DeckListView(ListView):
    model = Deck
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # The collected url param only applies to login users
        # Therefore, ask for login if used by anon user
        collected_param = request.GET.get("collected")

        if collected_param and not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(Q(creator=self.request.user.id) | Q(private=False))
            .select_related("creator")
            .annotate(card_count=Count("cards"))
            .order_by("-create_date")
        )

        search_param = self.request.GET.get("search")

        if search_param:
            queryset = queryset.filter(title__icontains=search_param)

        creator_id_param = self.request.GET.get("creator_id")

        if creator_id_param and creator_id_param.isdigit():
            creator_id = int(creator_id_param)
            queryset = queryset.filter(creator=creator_id)

        # If collected_param defined here, user is logged in
        collected_param = self.request.GET.get("collected")

        if collected_param == "true":
            queryset = queryset.filter(users=self.request.user.id)

        elif collected_param == "false":
            queryset = queryset.exclude(users=self.request.user.id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_context_headings(context, "Decks")
        return context
