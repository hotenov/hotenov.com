"""Test fixtures for all tests."""
import pytest


@pytest.fixture
def site_domain(request, db):
    """Get site domain value."""
    from django.contrib.sites.models import Site

    # "example.com" is the default value in fresh database
    default_domain = Site.objects.get_current().domain
    marker = request.node.get_closest_marker("custom_domain")
    if marker is None:
        domain = default_domain
    else:
        domain = str(marker.args[0])
    return domain


# @pytest.fixture
# def new_site(site_domain, db):
#     """Create new site record."""
#     from django.contrib.sites.models import Site

# # ERROR (after adding a migration with changing default site name):
# # django.db.utils.IntegrityError: duplicate key value violates unique constraint "django_site_pkey"  # noqa: B950
#     # new_site = Site.objects.create(domain=site_domain, name=site_domain)
#     obj, created = Site.objects.get_or_create(domain=site_domain, defaults={"name": site_domain})  # noqa: B950
#     return obj

# Fixture after adding migration with custom default site name
# To avoid integrity error (but maybe the migration was a wrong way)
@pytest.fixture(scope="function")
def django_db_setup_with_custom_domain(django_db_setup, django_db_blocker, site_domain):
    """Change default domain in DB for a particular test."""
    from django.contrib.sites.models import Site

    with django_db_blocker.unblock():
        Site.objects.update_or_create(
            pk=1,
            defaults={"name": site_domain, "domain": site_domain},
        )
