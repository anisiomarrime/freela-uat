# Generated by Django 2.2.7 on 2020-05-01 13:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mozlancers', '0030_auto_20200501_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentpackage',
            name='expire_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]