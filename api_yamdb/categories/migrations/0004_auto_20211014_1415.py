# Generated by Django 2.2.16 on 2021-10-14 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20211014_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
