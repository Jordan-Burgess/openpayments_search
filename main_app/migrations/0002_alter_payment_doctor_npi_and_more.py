# Generated by Django 5.0.2 on 2024-02-27 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='doctor_npi',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='doctor_profile_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='submitting_manufacturer_id',
            field=models.BigIntegerField(),
        ),
    ]