# Generated by Django 3.1.1 on 2020-10-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_examApp', '0002_auto_20201015_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='users_joining',
            field=models.ManyToManyField(related_name='trips', to='belt_examApp.User'),
        ),
    ]
