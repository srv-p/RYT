# Generated by Django 4.1.6 on 2023-04-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_event_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dept_name',
            field=models.CharField(choices=[('Stores', 'Stores'), ('Kitchen', 'Kitchen'), ('Holistic Health', 'Holistic Health'), ('Aura', 'Aura'), ('Maintenance', 'Maintenance'), ('Altar', 'Altar'), ('Ankur', 'Ankur'), ('Hostel Essentials', 'Hostel Essentials'), ('Multimedia', 'Multimedia'), ('Music', 'Music'), ('Telephone', 'Telephone'), ('Sai Replica', 'Sai Replica'), ('Sports', 'Sports'), ('InSaight', 'InSaight'), ('Cardroom', 'Cardroom')], max_length=20),
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
