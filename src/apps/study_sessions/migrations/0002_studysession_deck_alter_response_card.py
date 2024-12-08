# Generated by Django 5.1.1 on 2024-12-03 04:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("decks", "0002_alter_deck_creator"),
        ("study_sessions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="studysession",
            name="deck",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="study_sessions",
                to="decks.deck",
            ),
        ),
        migrations.AlterField(
            model_name="response",
            name="card",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="responses",
                to="decks.card",
            ),
        ),
    ]
