# Generated by Django 5.2.1 on 2025-05-20 00:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(db_index=True, max_length=100)),
            ],
            options={
                "db_table": "genre",
            },
        ),
    ]
