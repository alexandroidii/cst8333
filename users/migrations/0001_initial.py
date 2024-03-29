# Generated by Django 3.2 on 2021-04-20 18:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('rlcs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('user_name', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=25, verbose_name='first name')),
                ('last_name', models.CharField(max_length=25, verbose_name='last name')),
                ('phone_number', phone_field.models.PhoneField(blank=True, max_length=25, verbose_name='phone number')),
                ('company_name', models.CharField(blank=True, max_length=50, verbose_name='company name')),
                ('position', models.CharField(blank=True, max_length=50, verbose_name='position')),
                ('website', models.CharField(blank=True, max_length=50, verbose_name='website')),
                ('address', models.CharField(blank=True, max_length=50, verbose_name='address')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='city')),
                ('province_state', models.CharField(blank=True, max_length=20, verbose_name='province')),
                ('country', models.CharField(blank=True, max_length=20, verbose_name='country')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('about', models.TextField(blank=True, max_length=500, verbose_name='about')),
                ('is_reviewer', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('industry_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rlcs.industrytype')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'CCS Users',
            },
        ),
    ]
