from django.forms import ModelForm, Textarea

from .models import Card, Deck


class DeckForm(ModelForm):
    class Meta:
        model = Deck
        fields = ["title", "private"]


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = ["question", "answer"]
        widgets = {
            "question": Textarea(attrs={"rows": 5}),
            "answer": Textarea(attrs={"rows": 5}),
        }
