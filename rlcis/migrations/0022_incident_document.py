# Generated by Django 3.1.4 on 2021-01-04 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rlcis', '0021_document_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rlcis.document'),
        ),
    ]
