# Generated by Django 5.1.1 on 2025-01-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("study_sessions", "0003_alter_response_is_correct"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studysession",
            name="create_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
