# Generated by Django 3.0.8 on 2020-08-28 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogg', '0008_auto_20200828_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='blog',
            name='likes',
        ),
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]