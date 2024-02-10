# Generated by Django 5.0.1 on 2024-02-08 06:52

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField()),
                ('place', models.CharField(max_length=100, verbose_name='Place to action')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Time to action')),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=120), verbose_name='Duration of action')),
                ('periodicity', models.CharField(choices=[(0, 'Daily'), (1, 'Every Monday'), (2, 'Every Tuesday'), (3, 'Every Wednesday'), (4, 'Every Thursday'), (5, 'Every Friday'), (6, 'Every Saturday'), (7, 'Every Sunday')], max_length=1, verbose_name='Periodicity of action')),
                ('reward', models.CharField(blank=True, max_length=100, null=True)),
                ('is_pleasant', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('related_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit', verbose_name='Related action')),
            ],
            options={
                'verbose_name': 'Habit',
                'verbose_name_plural': 'Habits',
            },
        ),
    ]