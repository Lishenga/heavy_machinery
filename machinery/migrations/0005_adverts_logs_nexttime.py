# Generated by Django 2.1.2 on 2018-11-17 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machinery', '0004_pricing_adverts_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='adverts_logs',
            name='nexttime',
            field=models.DateField(default=None),
        ),
    ]
