# Generated by Django 3.2.12 on 2023-02-09 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20230209_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institute_applied',
            name='institute_name',
        ),
        migrations.AddField(
            model_name='institute_applied',
            name='institute_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.institutes'),
        ),
    ]