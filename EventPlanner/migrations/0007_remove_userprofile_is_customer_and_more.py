# Generated by Django 4.2.5 on 2023-09-13 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventPlanner', '0006_alter_userprofile_contact_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_customer',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_event_planner',
        ),
    ]