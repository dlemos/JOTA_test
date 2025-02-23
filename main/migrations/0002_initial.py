# Generated by Django 5.1.6 on 2025-02-20 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='verticals',
            field=models.ManyToManyField(help_text='Categories of PRO news this subscriber have access to', to='news.category'),
        ),
        migrations.AddField(
            model_name='user',
            name='subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.subscription'),
        ),
    ]
