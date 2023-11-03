# Generated by Django 3.1.6 on 2023-06-17 12:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20230614_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('source_stream', models.PositiveSmallIntegerField(choices=[(1, 'viator'), (2, 'airbnb'), (3, 'tripadvisor'), (4, 'expedia'), (5, 'klook'), (6, 'civitatis'), (7, 'getyourguide'), (8, 'facebook'), (9, 'google'), (10, 'instagram'), (11, 'linkedin'), (12, 'tiquets')])),
                ('review_text', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('sentiment', models.PositiveSmallIntegerField(choices=[(3, 'Positive'), (2, 'Neutral'), (1, 'Negative')], null=True)),
                ('review_url', models.TextField(null=True)),
                ('ai_checked', models.BooleanField(default=False)),
                ('responded', models.BooleanField(default=False)),
                ('product_id', models.CharField(max_length=255, null=True)),
                ('product', models.CharField(max_length=255, null=True)),
                ('country_code', models.CharField(max_length=255, null=True)),
                ('places', models.TextField(null=True)),
                ('img', models.TextField(null=True)),
                ('can_respond', models.BooleanField(default=False)),
            ],
        ),
    ]
