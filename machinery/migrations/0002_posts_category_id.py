# Generated by Django 2.1.2 on 2018-11-12 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machinery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='category_id',
            field=models.IntegerField(default=1),
        ),
    ]