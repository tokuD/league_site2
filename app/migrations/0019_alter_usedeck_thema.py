# Generated by Django 3.2 on 2021-04-30 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_usedeck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedeck',
            name='thema',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='app.deckthema'),
        ),
    ]
