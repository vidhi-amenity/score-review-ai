# Generated by Django 3.1.6 on 2023-07-04 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_toururl_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tour', to='api.tour'),
        ),
    ]
