# Generated by Django 3.1.4 on 2021-02-03 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rlcis', '0026_incidentdocument_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentdocument',
            name='name',
        ),
    ]
