# Generated by Django 3.1.6 on 2023-08-17 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20230725_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.tour'),
        ),
    ]
