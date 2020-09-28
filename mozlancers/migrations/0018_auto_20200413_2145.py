# Generated by Django 2.2.7 on 2020-04-13 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mozlancers', '0017_auto_20200409_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_reward', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BugType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('reward', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward', models.DecimalField(decimal_places=2, max_digits=2)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('bug_report', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='mozlancers.BugReport')),
                ('reward_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bugreport',
            name='bug_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='mozlancers.BugType'),
        ),
        migrations.AddField(
            model_name='bugreport',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]