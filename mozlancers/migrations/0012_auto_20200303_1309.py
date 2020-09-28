# Generated by Django 2.2.7 on 2020-03-03 13:09

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mozlancers', '0011_auto_20200229_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freelancerstats',
            name='last_login',
        ),
        migrations.AddField(
            model_name='employer',
            name='payment_verified',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='literaryskills',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 3, 13, 9, 11, 467187, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='literaryskills',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 3, 13, 9, 11, 467135, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='FreelaReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(default='')),
                ('rate', models.IntegerField(default=0)),
                ('employer', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='mozlancers.Employer')),
                ('freelancer', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='mozlancers.Freelancer')),
            ],
        ),
    ]
