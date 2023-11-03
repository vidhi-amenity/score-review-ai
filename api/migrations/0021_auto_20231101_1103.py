# Generated by Django 3.1.6 on 2023-11-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20231012_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='category_id',
        ),
        migrations.AlterField(
            model_name='tour',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Non Classified')], default=0),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
