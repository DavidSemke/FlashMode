from django.urls import path

from .views.card_edit import CardCreateView, CardDeleteView, CardUpdateView
from .views.card_list import CardListView
from .views.deck_detail import DeckDetailView
from .views.deck_edit import DeckCreateView, DeckDeleteView, DeckUpdateView
from .views.deck_list import DeckListView

app_name = "decks"
urlpatterns = [
    path("", DeckListView.as_view(), name="deck_list"),
    path("create/", DeckCreateView.as_view(), name="deck_create"),
    path("<int:deck_id>/", DeckDetailView.as_view(), name="deck_detail"),
    path("<int:deck_id>/update/", DeckUpdateView.as_view(), name="deck_update"),
    path("<int:deck_id>/delete/", DeckDeleteView.as_view(), name="deck_delete"),
    path("<int:deck_id>/cards/", CardListView.as_view(), name="card_list"),
    path("<int:deck_id>/cards/create/", CardCreateView.as_view(), name="card_create"),
    path(
        "<int:deck_id>/cards/<int:card_id>/update/",
        CardUpdateView.as_view(),
        name="card_update",
    ),
    path(
        "<int:deck_id>/cards/<int:card_id>/delete/",
        CardDeleteView.as_view(),
        name="card_delete",
    ),
]
