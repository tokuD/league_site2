# Generated by Django 3.2 on 2021-05-04 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_auto_20210504_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchrecord',
            name='deck1',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='deck2',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='point1',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='point2',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='results1',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='results2',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='score1',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='score2',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='skill1',
        ),
        migrations.RemoveField(
            model_name='matchrecord',
            name='skill2',
        ),
        migrations.AlterField(
            model_name='matchrecord',
            name='player1',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='matchrecord',
            name='player2',
            field=models.JSONField(),
        ),
    ]
