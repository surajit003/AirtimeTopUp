# Generated by Django 3.1.2 on 2020-10-14 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("message", "0003_auto_20201012_0725"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileUpload",
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
                ("name", models.CharField(blank=True, max_length=255)),
                ("document", models.FileField(upload_to="documents/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
