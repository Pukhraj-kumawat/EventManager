# Generated by Django 4.2.5 on 2023-10-22 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventPlanner', '0011_remove_userprofile_otp_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='otp_verified',
            field=models.BooleanField(default=False),
        ),
    ]