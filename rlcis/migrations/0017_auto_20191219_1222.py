# Generated by Django 2.2.7 on 2019-12-19 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rlcis', '0016_auto_20191218_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='country',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='location',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='region',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
