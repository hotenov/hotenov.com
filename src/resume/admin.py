"""Admin models for 'resume' app."""
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.admin import TranslationStackedInline

from .models import Certificate
from .models import Education
from .models import Job
from .models import Resume


# class JobInline(admin.TabularInline):
class JobInline(TranslationStackedInline):
    """Job admin inline form."""

    model = Job
    ordering = ("-start_date", "-quit_date")
    extra = 1


class ResumeAdmin(admin.ModelAdmin):
    """Resume admin form object."""

    # fields = [
    #     "role",
    #     "slug",
    #     "search_status",
    #     "is_published",
    #     "person_name",
    #     "photo",
    #     "contact_info",
    #     "social_links",
    #     "personal_profile",
    #     "skills",
    #     "education",
    #     "writings",
    #     "contributions",
    #     "hobby",
    #     "certifications",
    #     "personal_projects",
    #     "languages",
    #     "created_at",
    #     "updated_at",
    # ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "role",
                    "slug",
                    "search_status",
                    "is_published",
                    "display_on_main",
                ]
            },
        ),
        (
            "Person info",
            {
                "fields": [
                    "person_name",
                    "photo",
                    "contact_info",
                    "social_links",
                ]
            },
        ),
        (
            "Skills and Expirience",
            {
                "fields": [
                    "personal_profile",
                    "skills_summary",
                    "skills",
                    "relevant_skills",
                    "educations",
                    "writings",
                    "contributions",
                    "hobby",
                    "certifications",
                    "personal_projects",
                    "languages",
                ]
            },
        ),
        (
            "Date information",
            {
                "fields": [
                    "updated_at",
                    "created_at",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Shared Files",
            {
                "fields": [
                    "file_pdf",
                ],
            },
        ),
    ]

    readonly_fields = ["created_at"]

    prepopulated_fields = {"slug": ("role",)}

    inlines = [JobInline]

    list_display = [
        "id",
        "role",
        "slug",
        "search_status",
        "updated_at",
        "is_published",
        "display_on_main",
    ]
    list_display_links = ["id", "role"]
    list_editable = ["is_published", "display_on_main"]

    search_fields = ["role"]
    list_filter = ["is_published", "search_status"]

    # Admin Save buttons
    save_as = True
    save_on_top = True


class MyTranslatedResumeAdmin(ResumeAdmin, TabbedTranslationAdmin):
    """ResumeAdmin with inherited translation options."""

    pass


class EducationAdmin(admin.ModelAdmin):
    """Education admin form object."""

    list_display = [
        "id",
        "title",
        "degree",
        "start_date",
        "end_date",
    ]

    list_display_links = ["id", "title"]

    search_fields = ["title"]

    save_on_top = True


class TranslatedEducationAdmin(EducationAdmin, TabbedTranslationAdmin):
    """EducationAdmin with inherited translation options."""

    pass


class CertificateAdmin(admin.ModelAdmin):
    """Certificate admin object."""

    list_display = [
        "id",
        "title",
        "credential_id",
        "issue_date",
    ]

    list_display_links = ["id", "title"]

    search_fields = ["title", "credential_id"]

    save_on_top = True


class TranslatedCertificateAdmin(CertificateAdmin, TabbedTranslationAdmin):
    """CertificateAdmin with inherited translation options."""

    pass


admin.site.register(Resume, MyTranslatedResumeAdmin)
admin.site.register(Education, TranslatedEducationAdmin)
admin.site.register(Certificate, TranslatedCertificateAdmin)
