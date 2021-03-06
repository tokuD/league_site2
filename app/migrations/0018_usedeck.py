# Generated by Django 3.2 on 2021-04-30 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0017_alter_character_world'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseDeck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='decks')),
                ('image2', models.ImageField(blank=True, upload_to='decks')),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('thema', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.deckthema')),
            ],
        ),
    ]
