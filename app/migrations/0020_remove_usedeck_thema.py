# Generated by Django 3.2 on 2021-04-30 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_usedeck_thema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usedeck',
            name='thema',
        ),
    ]
