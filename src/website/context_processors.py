"""Context processors for 'website' app."""
from django.conf import settings


def debug_flag(request):
    """Add variable with DEBUG value."""
    return {"debug_flag": settings.DEBUG}
