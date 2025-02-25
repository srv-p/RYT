# Generated by Django 4.1.6 on 2023-03-14 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raise_tktapp', '0012_comments_model_commented_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='frqt_tkt_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(blank=True, max_length=15)),
                ('frqt_tkt_name', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='media/')),
                ('fields', models.JSONField()),
                ('is_available', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'frequently_raised_tkts_table',
            },
        ),
    ]
