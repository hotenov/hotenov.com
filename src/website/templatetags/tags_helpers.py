"""Custom website filters and tags."""
from django import template
from django.urls import reverse
from django.utils import translation


register = template.Library()


@register.simple_tag
def define(value=None):
    """Set value for template variable."""
    return value


@register.simple_tag(takes_context=True)
def get_default_lang_url(context, lang="ru"):
    """Return URL path without lang prefix."""
    req = context["request"]
    cut_lang_prefix = req.build_absolute_uri().replace(f"/{lang}/", "/", 1)
    return cut_lang_prefix


@register.inclusion_tag("website/customtags/link_alternate.html", takes_context=True)
def alternate_lang_links(context, route_name):
    """Paste <link> HTML tag for alternate URLs in available languages."""
    return {
        "request": context["request"],
        "route_name": route_name,
    }


def reverse_for_language(route, lang):
    """Returns reversed URL for passed route."""
    with translation.override(lang):
        reversed_url = reverse(route)
        return reversed_url
