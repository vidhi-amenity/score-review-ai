# Generated by Django 3.1.6 on 2023-07-04 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20230704_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='toururl',
            name='success',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
