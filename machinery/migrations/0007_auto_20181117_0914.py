# Generated by Django 2.1.2 on 2018-11-17 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machinery', '0006_auto_20181117_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adverts',
            name='created_at',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
