# Generated by Django 2.2.7 on 2020-01-31 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mozlancers', '0008_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mozlancers.City'),
        ),
    ]
