# Generated by Django 5.1.1 on 2024-12-09 05:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("decks", "0002_alter_deck_creator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deck",
            name="title",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
