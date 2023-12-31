# Generated by Django 3.2.2 on 2021-05-13 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('what', '0005_work'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('sequence', models.IntegerField(default=1)),
                ('key', models.CharField(default='C', max_length=10)),
                ('is_ensemble', models.BooleanField(default=False)),
                ('parent_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='what.instrument')),
            ],
        ),
        migrations.CreateModel(
            name='WorkVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_original', models.BooleanField()),
                ('alt_name', models.CharField(max_length=100, null=True)),
                ('alt_catalogue', models.CharField(max_length=20, null=True)),
                ('alt_catalogue_number', models.IntegerField(null=True)),
                ('alt_date', models.CharField(max_length=30, null=True)),
                ('alt_tonality', models.CharField(max_length=30, null=True)),
                ('arranger_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='what.composer')),
            ],
        ),
        migrations.CreateModel(
            name='WorkVersionEnsemble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('instrument_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='what.instrument')),
                ('work_version_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='what.workversion')),
            ],
        ),
        migrations.AddField(
            model_name='workversion',
            name='instruments_ids',
            field=models.ManyToManyField(through='what.WorkVersionEnsemble', to='what.Instrument'),
        ),
        migrations.AddField(
            model_name='workversion',
            name='work_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='what.work'),
        ),
    ]
