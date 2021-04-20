# Generated by Django 3.2 on 2021-04-20 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rlcs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='reviewer',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_reviewer': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scenario',
            name='submitter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitter', to=settings.AUTH_USER_MODEL),
        ),
    ]