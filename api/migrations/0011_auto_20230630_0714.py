# Generated by Django 3.1.6 on 2023-06-30 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20230630_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='rating',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='tour',
            name='rating_override',
            field=models.BooleanField(default=False),
        ),
    ]
