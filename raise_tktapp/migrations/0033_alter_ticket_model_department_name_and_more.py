# Generated by Django 4.1.6 on 2023-04-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0032_alter_frqt_tkt_model_dept_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_model',
            name='Department_Name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='ticket_model',
            name='Title',
            field=models.CharField(max_length=50),
        ),
    ]
