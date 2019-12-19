# Generated by Django 2.2.7 on 2019-12-19 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rlcis', '0017_auto_20191219_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='bribe_type',
            field=models.CharField(choices=[('CA', 'Cash'), ('FA', 'Favors'), ('GR', 'Gratuity'), ('GI', 'Gifts'), ('OT', 'Other Bribe Type')], max_length=2),
        ),
        migrations.AlterField(
            model_name='incident',
            name='bribed_by',
            field=models.CharField(choices=[('AG', 'Agent'), ('TP', 'Third Party'), ('PO', 'Public Official'), ('OT', 'Bribed by Other')], max_length=2),
        ),
        migrations.AlterField(
            model_name='incident',
            name='industry_type',
            field=models.CharField(choices=[('AD', 'Advertising'), ('AG', 'Agriculture'), ('CN', 'Construction'), ('CM', 'Communications'), ('ED', 'Education'), ('EN', 'Entertainment'), ('FA', 'Fasion'), ('FI', 'Finance'), ('IT', 'Information Technology'), ('MA', 'Manufacturing'), ('RE', 'Retail'), ('TE', 'Technology'), ('TR', 'Transportation'), ('OT', 'Other Transportation Type')], max_length=2),
        ),
    ]
