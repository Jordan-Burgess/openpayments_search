# Generated by Django 5.0.3 on 2024-03-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_metadata_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='identifier',
            field=models.BigIntegerField(default=10),
            preserve_default=False,
        ),
    ]