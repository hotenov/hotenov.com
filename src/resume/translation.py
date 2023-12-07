"""Configuration for translated resume app models."""
from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import translator

from .models import Certificate
from .models import Education
from .models import Job
from .models import Resume


class ResumeTranslationOptions(TranslationOptions):
    """Translation options for Resume model."""

    fields = [
        "role",
        "person_name",
        "contact_info",
        "social_links",
        "personal_profile",
        "skills_summary",
        "skills",
        "relevant_skills",
        "writings",
        "contributions",
        "hobby",
        "personal_projects",
        "languages",
        "file_pdf",
    ]


class JobTranslationOptions(TranslationOptions):
    """Translation options for Job model."""

    fields = [
        "role",
        "company",
        "location",
        "description",
    ]


class EducationTranslationOptions(TranslationOptions):
    """Translation options for Education model."""

    fields = [
        "title",
        "degree",
        "study_field",
        "description",
        "activities",
        "location",
    ]


class CertificateTranslationOptions(TranslationOptions):
    """Translation options for Certificate model."""

    fields = [
        "title",
        "organization",
        "location",
        "commentary",
    ]


translator.register(Resume, ResumeTranslationOptions)
translator.register(Job, JobTranslationOptions)
translator.register(Education, EducationTranslationOptions)
translator.register(Certificate, CertificateTranslationOptions)
