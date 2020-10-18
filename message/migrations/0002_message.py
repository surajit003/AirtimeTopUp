# Generated by Django 3.1.2 on 2020-10-12 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("message", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("1", "success"), ("0", "failure")], max_length=20
                    ),
                ),
                ("partner_message_id", models.CharField(max_length=80)),
                ("status_code", models.IntegerField()),
                ("recipient", models.CharField(max_length=40)),
                ("response", models.TextField()),
                (
                    "gateway",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="message.gateway",
                    ),
                ),
            ],
        ),
    ]