# Generated by Django 4.1.6 on 2023-04-15 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0037_alter_announcements_model_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket_model',
            name='image',
            field=models.FileField(blank=True, upload_to='tkts_files'),
        ),
    ]
