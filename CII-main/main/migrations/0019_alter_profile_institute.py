# Generated by Django 4.1.5 on 2023-01-22 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0018_alter_stud_data_upload_institute_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="institute",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="main.institutes",
            ),
        ),
    ]
