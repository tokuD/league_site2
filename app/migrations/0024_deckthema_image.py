# Generated by Django 3.2 on 2021-05-01 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_match_player1'),
    ]

    operations = [
        migrations.AddField(
            model_name='deckthema',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]