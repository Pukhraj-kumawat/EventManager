# Generated by Django 4.2.5 on 2023-09-30 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventPlanner', '0030_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
