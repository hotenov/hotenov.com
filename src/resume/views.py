"""Resume controllers (views)."""
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Resume


class ResumeIndexView(ListView):
    """Resume Index page view."""

    # model = Resume
    template_name = "resume/index.html"
    context_object_name = "resumes"

    def get_queryset(self):
        """Get filtered queryset Resume objects."""
        return Resume.objects.filter(
            display_on_main=True,
            is_published=True,
        ).order_by("-updated_at")

    def get_context_data(self, **kwargs):
        """Retrieve base context and add custom data."""
        context = super().get_context_data(**kwargs)
        resume_set = self.get_queryset()
        if len(resume_set) == 1:
            context["jobs"] = (
                resume_set.first()
                .jobs.filter(is_displayed=True)
                .order_by("-start_date", "-quit_date")
            )
            context["resume"] = resume_set.first()
        return context


class ResumeDetailView(DetailView):
    """View for single resume page (by slug)."""

    model = Resume
    template_name = "resume/single.html"
    context_object_name = "resume"

    def get_object(self):
        """Get object for detailed view."""
        # Get last updated Resume for main (index) page
        # in order to know its slug
        main_resumes = Resume.objects.filter(
            display_on_main=True,
            is_published=True,
        ).order_by("-updated_at")
        if main_resumes:
            pk = main_resumes.first().pk
        else:
            pk = 0
        last_updated = get_object_or_404(main_resumes, pk=pk)
        if "slug" not in self.kwargs:
            self.kwargs["slug"] = last_updated.slug
        return super().get_object()

    def get_context_data(self, **kwargs):
        """Retrieve base context and add custom data."""
        context = super().get_context_data(**kwargs)
        resume_obj = self.get_object()
        # Filter and order jobs for current Resume object
        context["jobs"] = resume_obj.jobs.filter(is_displayed=True).order_by(
            "-start_date",
            "-quit_date",
        )
        return context
