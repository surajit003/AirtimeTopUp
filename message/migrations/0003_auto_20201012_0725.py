# Generated by Django 3.1.2 on 2020-10-12 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("message", "0002_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="status",
            field=models.CharField(max_length=40),
        ),
    ]
