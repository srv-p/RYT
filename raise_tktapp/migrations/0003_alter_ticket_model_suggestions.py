# Generated by Django 4.1.5 on 2023-01-26 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0002_alter_ticket_model_dept_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_model',
            name='suggestions',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
