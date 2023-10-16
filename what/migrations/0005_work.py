# Generated by Django 3.2.2 on 2021-05-10 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('what', '0004_alter_composer_death'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oo_id', models.IntegerField(default=-1)),
                ('oo_genre', models.CharField(default='', max_length=40)),
                ('name', models.CharField(max_length=100)),
                ('subname', models.CharField(default='', max_length=100)),
                ('nickname', models.CharField(default='', max_length=60)),
                ('tonality', models.CharField(default='', max_length=30)),
                ('catalogue', models.CharField(default='', max_length=20)),
                ('catalogue_number', models.IntegerField(default=0)),
                ('date', models.CharField(default='', max_length=30)),
                ('is_popular', models.BooleanField(default=False)),
                ('is_essential', models.BooleanField(default=False)),
                ('composer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='what.composer')),
            ],
        ),
    ]
