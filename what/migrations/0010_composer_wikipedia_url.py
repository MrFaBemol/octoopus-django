# Generated by Django 3.2.2 on 2021-06-18 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('what', '0009_auto_20210613_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='composer',
            name='wikipedia_url',
            field=models.URLField(default='', max_length=230),
        ),
    ]