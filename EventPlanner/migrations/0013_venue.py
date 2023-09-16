# Generated by Django 4.2.5 on 2023-09-15 05:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EventPlanner', '0012_alter_userprofile_contact_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('state', models.CharField(choices=[('Rajasthan', 'Rajasthan'), ('Gujrat', 'Gujrat'), ('Madhya pradesh', 'Madhya pradesh'), ('Maharastra', 'Maharastra')], max_length=50)),
                ('service_offered', models.TextField()),
                ('vendors', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
