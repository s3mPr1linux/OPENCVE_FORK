# Generated by Django 4.2.3 on 2023-11-08 08:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0005_remove_organization_owner_alter_membership_key"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="membership",
            table="opencve_memberships",
        ),
    ]
