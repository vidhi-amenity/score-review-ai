# Generated by Django 3.1.6 on 2023-10-27 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20231012_1138'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='tour',
        #     name='category',
        # ),
        # migrations.RemoveField(
        #     model_name='tour',
        #     name='category_id',
        # ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
