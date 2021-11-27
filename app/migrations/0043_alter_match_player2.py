# Generated by Django 3.2 on 2021-05-03 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0042_auto_20210503_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='player2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='player2', to=settings.AUTH_USER_MODEL),
        ),
    ]