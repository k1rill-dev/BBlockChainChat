# Generated by Django 4.1.3 on 2022-11-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='hash_bloks',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
