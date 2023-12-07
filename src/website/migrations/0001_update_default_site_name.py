"""Migration to change default site name."""
from django.conf import settings
from django.db import migrations


def forwards_func(apps, schema_editor):
    """Set up or rename the default example.com site created by Django."""
    Site = apps.get_model("sites", "Site")
    db_alias = schema_editor.connection.alias
    Site.objects.using(db_alias).update_or_create(
        pk=settings.SITE_ID,
        defaults={
            "name": settings.SITE_NAME,
            "domain": settings.SITE_DOMAIN,
        },
    )


def reverse_func(apps, schema_editor):
    """Reverse the default site name."""
    Site = apps.get_model("sites", "Site")
    db_alias = schema_editor.connection.alias
    Site.objects.using(db_alias).update_or_create(
        pk=settings.SITE_ID,
        defaults={
            "name": settings.DEFAULT_SITE_DOMAIN,
            "domain": settings.DEFAULT_SITE_DOMAIN,
        },
    )


class Migration(migrations.Migration):
    """Update or revert default name site."""

    dependencies = [
        # ("your_app", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
