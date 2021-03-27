# Generated by Django 3.1.7 on 2021-03-27 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BribedBy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BribeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IndustryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LevelOfAuthority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
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
            name='Scenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('scenario_summary', models.CharField(max_length=200, null=True)),
                ('scenario_details', models.TextField(null=True)),
                ('risks', models.TextField(null=True)),
                ('resolution', models.TextField(null=True)),
                ('country', models.CharField(blank=True, max_length=60, null=True)),
                ('region', models.CharField(blank=True, max_length=60, null=True)),
                ('location', models.CharField(blank=True, max_length=60, null=True)),
                ('first_occurence', models.DateField(blank=True, null=True)),
                ('resolution_date', models.DateField(blank=True, null=True)),
                ('anonymous', models.BooleanField(default=False, help_text='Would you like to submit this scenario Anonymously?', null=True)),
                ('is_training_scenario', models.BooleanField(default=False, help_text='Is this a real life Scenario or a Ficticous Scenario?')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('bribe_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rlcis.bribetype')),
                ('bribed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rlcis.bribedby')),
                ('industry_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rlcis.industrytype')),
                ('levelOfAuthority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rlcis.levelofauthority')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rlcis.reviewer')),
            ],
        ),
        migrations.CreateModel(
            name='ScenarioDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='scenarios/uploads/')),
                ('scenario', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rlcis.scenario')),
            ],
        ),
    ]
