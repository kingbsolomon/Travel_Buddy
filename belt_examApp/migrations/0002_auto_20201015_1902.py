# Generated by Django 3.1.1 on 2020-10-15 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_examApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='planned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planner', to='belt_examApp.user'),
        ),
    ]