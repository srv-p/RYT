# Generated by Django 4.1.6 on 2023-04-03 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0031_alter_frqt_tkt_model_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frqt_tkt_model',
            name='dept_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
