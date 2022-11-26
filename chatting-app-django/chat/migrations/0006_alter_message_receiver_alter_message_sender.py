# Generated by Django 4.1.3 on 2022-11-25 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0005_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="receiver",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receiver",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Получатель",
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sender",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Отправитель",
            ),
        ),
    ]
