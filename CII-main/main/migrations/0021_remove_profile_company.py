# Generated by Django 4.1.5 on 2023-01-22 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_profile_company_alter_profile_institute"),
    ]

    operations = [
        migrations.RemoveField(model_name="profile", name="company",),
    ]
