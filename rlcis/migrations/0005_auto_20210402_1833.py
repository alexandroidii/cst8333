# Generated by Django 3.1.7 on 2021-04-02 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rlcis', '0004_auto_20210331_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='reviewer',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_reviewer': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL),
        ),
    ]
