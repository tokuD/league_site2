# Generated by Django 3.2 on 2021-05-03 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0043_alter_match_player2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='player1',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='player2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='player2', to='users.user'),
            preserve_default=False,
        ),
    ]