# Generated by Django 2.2.7 on 2020-01-28 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mozlancers', '0002_auto_20200128_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='exp',
            field=models.IntegerField(default=0),
        ),
    ]