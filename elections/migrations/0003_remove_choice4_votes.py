# Generated by Django 2.0.6 on 2018-07-01 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_auto_20180702_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice4',
            name='votes',
        ),
    ]
