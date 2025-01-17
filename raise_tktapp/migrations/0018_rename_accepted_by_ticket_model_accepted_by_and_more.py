# Generated by Django 4.1.6 on 2023-03-23 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0017_alter_ticket_model_dept_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket_model',
            old_name='accepted_by',
            new_name='Accepted_By',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='created_at',
            new_name='Created_At',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='dept_name',
            new_name='Department_Name',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='desc',
            new_name='Description',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='raised_by',
            new_name='Raised_By',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='status',
            new_name='Status',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='suggestions',
            new_name='Suggestions',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='tkt_id',
            new_name='Ticket_ID',
        ),
        migrations.RenameField(
            model_name='ticket_model',
            old_name='title',
            new_name='Title',
        ),
    ]
