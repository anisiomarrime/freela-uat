# Generated by Django 2.2.7 on 2020-02-29 13:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mozlancers', '0010_auto_20200131_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='literaryskills',
            name='month',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='literaryskills',
            name='year',
            field=models.IntegerField(default=2020),
        ),
        migrations.AlterField(
            model_name='literaryskills',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2020, 2, 29, 13, 13, 33, 49059, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='literaryskills',
            name='institute',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='literaryskills',
            name='qualification',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='literaryskills',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2020, 2, 29, 13, 13, 33, 49012, tzinfo=utc)),
        ),
    ]
