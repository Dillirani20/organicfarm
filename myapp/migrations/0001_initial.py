# Generated by Django 4.2.16 on 2024-09-23 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mob_no",
                    models.CharField(blank=True, max_length=12, null=True, unique=True),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female"), ("o", "Others")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("is_seller", models.BooleanField(default=False)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="profiles/default.jpg",
                        null=True,
                        upload_to="profiles/",
                    ),
                ),
                ("joined_on", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]