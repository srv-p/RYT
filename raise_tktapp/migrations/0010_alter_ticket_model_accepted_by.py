# Generated by Django 4.1.6 on 2023-02-07 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0009_alter_ticket_model_accepted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_model',
            name='accepted_by',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
