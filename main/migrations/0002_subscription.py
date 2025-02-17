# Generated by Django 5.1.6 on 2025-02-17 15:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        ('news', '0002_remove_news_pubblising_date_news_publising_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('I', 'JOTA Info'), ('P', 'JOTA PRO')], max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('verticals', models.ManyToManyField(to='news.category')),
            ],
        ),
    ]
