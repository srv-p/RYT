# Generated by Django 4.1.6 on 2023-04-13 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0036_alter_ticket_model_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements_model',
            name='Created_At',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ticket_model',
            name='Accepted_By',
            field=models.CharField(default='To Be Accepted', max_length=20, null=True),
        ),
    ]
