# Generated by Django 4.1.3 on 2022-12-23 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vnz", "0011_delete_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/"),
        ),
    ]
