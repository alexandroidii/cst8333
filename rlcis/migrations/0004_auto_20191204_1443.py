# Generated by Django 2.2.7 on 2019-12-04 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rlcis', '0003_auto_20191204_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='incident_details',
            field=models.TextField(default='not filled in', null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='incident_summary',
            field=models.CharField(default='not filled in', max_length=200, null=True),
        ),
    ]
