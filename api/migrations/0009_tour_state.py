# Generated by Django 3.1.6 on 2023-06-30 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_tour_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
    ]