# Generated by Django 2.2.7 on 2019-12-19 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rlcis', '0014_auto_20191218_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='industry_type_other',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
