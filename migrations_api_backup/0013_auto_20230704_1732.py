# Generated by Django 3.1.6 on 2023-07-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_merge_20230704_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tour',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='toururl',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
