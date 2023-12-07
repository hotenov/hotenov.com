"""Custom sitemap classes."""
from django.contrib import sitemaps
from django.urls import reverse

from resume.models import Resume


class StaticViewSitemap(sitemaps.Sitemap):
    """Generates sitemap entries for static pages."""

    priority = 0.5
    changefreq = "daily"
    protocol = "https"
    i18n = True
    alternates = True

    def items(self):
        """Override base method placing named static routes."""
        return [
            "website:index",
            "website:about",
            "website:contact",
            "website:tms-review-2019",
            "resume:index",
        ]

    def location(self, item):
        """Get location for overridden item."""
        return reverse(item)


class ResumeSitemap(sitemaps.Sitemap):
    """Generates sitemap entries for Resume published entries."""

    priority = 0.7
    changefreq = "monthly"
    protocol = "https"
    i18n = True
    alternates = True

    def items(self):
        """Get only published resume entries."""
        return Resume.objects.filter(is_published=True)

    def lastmod(self, obj):
        """Get lastmod date for model object."""
        return obj.updated_at
