# Generated by Django 2.2.7 on 2019-11-30 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('employee_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=60)),
                ('region', models.CharField(max_length=60)),
                ('bribed_by', models.CharField(max_length=100)),
                ('bribed_by_other', models.CharField(max_length=100)),
                ('bribe_type', models.CharField(max_length=60)),
                ('bribe_type_other', models.CharField(max_length=60)),
                ('location', models.CharField(max_length=60)),
                ('first_occurence', models.DateTimeField(verbose_name='first occurence')),
                ('resolution_date', models.DateTimeField(verbose_name='resolution date')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rlcis.Reviewer')),
            ],
        ),
    ]
