"""Models in 'resume' app."""
from datetime import date

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ResumeManager(models.Manager):
    """Model manager for Resume model."""

    def get_by_natural_key(self, slug):
        """Get Resume record by its natural key (not standard primary key)."""
        return self.get(slug=slug)


class Resume(models.Model):
    """Represents resume (cv) object."""

    class SearchingJobStatus(models.IntegerChoices):
        """Fixed choices of current job searching status."""

        WORK = 0, _("Open to work")
        NEW_OPPORTUNITIES = 1, _("Open to new opportunities")
        NOT_AVAILABLE = 2, _("Not available to be hired")
        READY_TO_PART_TIME = 3, _("Work now, but ready to another part-time job")
        UNKNOWN = 4, _("Unknown")

    objects = ResumeManager()

    role = models.CharField("Role", max_length=255)
    slug = models.SlugField("URL", max_length=255, unique=True)
    search_status = models.IntegerField(
        "Search status", choices=SearchingJobStatus.choices, default=0
    )
    is_published = models.BooleanField("Is Published?", default=False)
    display_on_main = models.BooleanField("Display on Main?", default=False)

    person_name = models.CharField("Full Name", max_length=255)
    photo = models.ImageField(upload_to="resume/profiles/", blank=True)

    contact_info = models.TextField(
        "Contact Information",
        blank=True,
        help_text="One contact per line as Title||URL||fa_icon_class(es)",
    )
    social_links = models.TextField(
        "Links",
        blank=True,
        help_text=(
            "One link per line as Title||URL||fa_icon_class(es)<br>"
            "<br>"
            "Examples of CSS classes for icons:"
            "'fa-brands fa-linkedin-in', "
            "'fa-brands fa-twitter', "
            "'fa-solid fa-globe', "
            "'fa-brands fa-facebook' and other Font Awesome icons <br>"
            "Examples of custom CSS classes for icons:"
            "'brand-habr-career'"
        ),
    )

    personal_profile = models.TextField("Profile / About", blank=True)

    # For career change resume
    skills_summary = models.TextField(
        "Skills Summary",
        blank=True,
        help_text="HTML tags are allowed here.",
    )

    skills = models.TextField(
        "Skills",
        blank=True,
        help_text="One skill per line as skill=89",
    )
    relevant_skills = models.TextField(
        "Relevant Skills (Instruments)",
        blank=True,
        help_text="One skill / instrument per line as Category: skill1, skill2, ...",
    )
    # education = models.TextField("Education", blank=True)
    educations = models.ManyToManyField(
        "Education",
        blank=True,
        related_name="resumes",
    )
    writings = models.TextField("Writings", blank=True)
    contributions = models.TextField("Contributions", blank=True)
    hobby = models.TextField(
        "Interests & Hobbies",
        blank=True,
        help_text="One activity per line.",
    )
    # certifications = models.TextField("Certifications", blank=True)
    certifications = models.ManyToManyField(
        "Certificate",
        blank=True,
        related_name="resumes",
    )
    personal_projects = models.TextField(
        "Personal Projects",
        blank=True,
        help_text="HTML tags are allowed here.",
    )
    languages = models.CharField(
        "Languages",
        blank=True,
        default="English (B?); Russian (native)",
        max_length=255,
        help_text="Semicolon separated list as English (B2); Russian (native)",
    )
    # author = models.CharField("Author", max_length=100)  # TODO: set username
    created_at = models.DateTimeField("Created", auto_now_add=True)

    updated_at = models.DateTimeField("Updated", default=timezone.now)

    file_pdf = models.FileField(
        "PDF File",
        upload_to="resume/files/",
        max_length=512,
        blank=True,
    )

    class Meta:
        """Meta attributes for Resume model."""

        verbose_name = "Resume"
        verbose_name_plural = "Resumes"
        ordering = ["-created_at", "role"]

    def natural_key(self):
        """Return natural key."""
        return (self.slug,)

    def __str__(self):
        """String representation of Resume object."""
        return self.role

    def get_absolute_url(self):
        """Retrieve object absolute URL by its slug."""
        return reverse("resume:detail", kwargs={"slug": self.slug})


class JobManager(models.Manager):
    """Model manager for Job model."""

    def get_by_natural_key(self, resume, company, role, start_date):
        """Get Job record by its natural key (not standard primary key)."""
        return self.get(
            resume=resume, company=company, role=role, start_date=start_date
        )


class Job(models.Model):
    """Represents job (work experience) object."""

    class EmploymentType(models.IntegerChoices):
        """Fixed choices of employment type."""

        FULL_TIME = 0, "full-time"
        PART_TIME = 1, "part-time"
        SELF_EMPLOYED = 2, "self-employed"
        FREELANCE = 3, "freelance"
        CONTRACT = 4, "contract"
        INTERNSHIP = 5, "internship"
        APPRENTICESHIP = 6, "apprenticeship"
        SEASONAL = 7, "seasonal"
        __empty__ = "(Unknown)"

    class WorkplaceType(models.IntegerChoices):
        """Fixed choices of workplace type."""

        REMOTE = 0, "remote"
        ON_SITE = 1, "on-site"
        HYBRID = 2, "hybrid"
        __empty__ = "(Unknown)"

    objects = JobManager()

    resume = models.ForeignKey(
        "Resume",
        on_delete=models.CASCADE,
        related_name="jobs",
        verbose_name="resume",
    )
    role = models.CharField("Role", max_length=200)
    company = models.CharField("Company Name", max_length=200)
    employment_type = models.IntegerField(
        "Employment Type", choices=EmploymentType.choices, default=0
    )
    workplace = models.IntegerField(
        "Workplace", choices=WorkplaceType.choices, default=0
    )
    start_date = models.DateField("Start Date", default=date.today)
    quit_date = models.DateField("Quit Date", default=date.today)
    logo = models.ImageField(upload_to="resume/jobs/", blank=True)
    website = models.URLField("Website", max_length=120, blank=True)
    location = models.CharField("Location", max_length=200, blank=True)
    is_current = models.BooleanField("Working here now", default=False)
    description = models.TextField("Description", blank=True)
    is_registered = models.BooleanField("Is Registered work expirience?", default=True)
    is_displayed = models.BooleanField("Is Displayed on the web page?", default=True)

    class Meta:
        """Meta attributes for Job model."""

        unique_together = [["resume", "company", "role", "start_date"]]

    def natural_key(self):
        """Return natural key."""
        return (self.resume, self.company, self.role, self.start_date)

    def __str__(self):
        """String representation of Job object."""
        return self.company


class Education(models.Model):
    """Education institution object."""

    title = models.CharField("Title", max_length=200)
    degree = models.CharField("Degree", max_length=200)
    study_field = models.CharField("Field of Study", max_length=120, blank=True)
    start_date = models.DateField("Start Date", default=date.today)
    end_date = models.DateField("End Date", default=date.today)
    description = models.TextField("Description", blank=True)
    grade = models.CharField("GPA", max_length=200, blank=True)
    activities = models.TextField("Activities and Societies", blank=True)
    location = models.CharField("Location", max_length=120, blank=True)

    class Meta:
        """Meta attributes for Education model."""

        ordering = ["-start_date"]

    def __str__(self):
        """String representation of Education object."""
        return self.title


class Certificate(models.Model):
    """Certificate object."""

    title = models.CharField("Title", max_length=200)
    organization = models.CharField("Issuing Organization", max_length=200, blank=True)
    is_expired = models.BooleanField("Does it expire?", default=False)
    issue_date = models.DateField("Issue Date", default=date.today)
    expiration_date = models.DateField("Expiration Date", default=date.today)
    credential_id = models.CharField("Credential ID", max_length=120, blank=True)
    credential_url = models.URLField("Credential URL", max_length=512, blank=True)
    picture = models.ImageField(upload_to="resume/certificates/", blank=True)
    location = models.CharField("Location", max_length=120, blank=True)
    commentary = models.CharField("Commentary", max_length=512, blank=True)

    class Meta:
        """Meta attributes for Certificate model."""

        ordering = ["-issue_date"]

    def __str__(self):
        """String representation of Certificate object."""
        return self.title
