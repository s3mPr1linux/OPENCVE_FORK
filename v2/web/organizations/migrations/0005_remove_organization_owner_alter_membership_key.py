# Generated by Django 4.2.3 on 2023-11-06 22:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0004_alter_organization_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organization",
            name="owner",
        ),
        migrations.AlterField(
            model_name="membership",
            name="key",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
