# Generated by Django 3.2 on 2021-05-04 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_result_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]