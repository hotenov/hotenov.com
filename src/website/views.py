"""Request controllers of 'website' app."""
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.conf import settings


class IndexView(TemplateView):
    """Template class-based view for 'Home' page."""

    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        """Get and update view context."""
        context = super().get_context_data(**kwargs)
        if self.request.LANGUAGE_CODE == "ru":
            context["page_title"] = "Главная"
            context["page_description"] = "Хотенов Артём @hotenov, разработчик ПО, личный сайт, блог. Фанат Python (Django). Руководство командой разработки. Software Engineer"  # noqa: B950
            context["page_keywords"] = "Питон разработчик, веб-разработка, программист, резюме, блог, проекты"  # noqa: B950
        else:
            context["page_title"] = "Home"
            context["page_description"] = "Artem Hotenov, Software Engineer. Personal website, blog, projects, about. Python (Django) lover. IT Project manager."  # noqa: B950
            context["page_keywords"] = "software engineer, python, django, resume, web development"  # noqa: B950
        return context


class AboutView(TemplateView):
    """Template class-based view for 'About' page."""

    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        """Get and update view context."""
        context = super().get_context_data(**kwargs)
        if self.request.LANGUAGE_CODE == "ru":
            context["page_title"] = "О себе"
            context["page_description"] = "Немного о себе, хобби"  # noqa: B950, BLK100
            context["page_keywords"] = "хобби, информационные технологии, программирование, сериалы, dj, миксы"  # noqa: B950
        else:
            context["page_title"] = "About"
            context["page_description"] = "About me (@hotenov). Hobby, free time activity"  # noqa: B950
            context["page_keywords"] = "hobby, IT, programming, software, free time, dj sets, music mixes"  # noqa: B950
        return context


class ContactView(TemplateView):
    """Template class-based view for 'Contact' page."""

    template_name = "website/contact.html"

    def get_context_data(self, **kwargs):
        """Get and update view context."""
        context = super().get_context_data(**kwargs)
        if self.request.LANGUAGE_CODE == "ru":
            context["page_title"] = "Контактная информация"
            context["page_description"] = "Как со мной связаться, написать мне на почту, социальные сети."  # noqa: B950, BLK100
            context["page_keywords"] = "контакты, информация, почта, обратная связь"  # noqa: B950
        else:
            context["page_title"] = "Contact"
            context["page_description"] = "My contact email"  # noqa: B950
            context["page_keywords"] = "contact info, email, social media"  # noqa: B950
        return context


class ResumeView(TemplateView):
    """Template class-based view for old resume page."""

    template_name = "website/resume.html"


class OldBlogView(TemplateView):
    """Template class-based view for old 'Blog' page."""

    template_name = "website/old_blog/posts.html"

    def get_context_data(self, **kwargs):
        """Get and update view context."""
        context = super().get_context_data(**kwargs)
        if self.request.LANGUAGE_CODE == "ru":
            context["page_title"] = "Блог"
            context["page_description"] = "блог @hotenov: разработка ПО, технологии"  # noqa: B950, BLK100
            context["page_keywords"] = "Питон разработка, веб-разработка, заметки программиста"  # noqa: B950
        else:
            context["page_title"] = "Blog"
            context["page_description"] = "blog @hotenov: Software Development. Technologies."  # noqa: B950
            context["page_keywords"] = "code notes, thoughts, web development"  # noqa: B950
        return context


class OldBlogPageView(TemplateView):
    """Template class-based view for 'TMS Review 2019' page."""

    template_name = "website/old_blog/tms-review-2019.html"

    def get_context_data(self, **kwargs):
        """Get and update view context."""
        context = super().get_context_data(**kwargs)
        if self.request.LANGUAGE_CODE == "ru":
            context["page_title"] = "Обзор систем управления тестированием в 2019, платные и бесплатные"  # noqa: B950
            context["page_description"] = "Для многих команд разработки рано или поздно встает вопрос о внедрении специализированных инструментов (систем) для управления процессом тестирования в своих проектах. Какой же из них выбрать? Рассмотрим 11 таких систем."  # noqa: B950
            context["page_keywords"] = "система управления, тестовые сценарии, тест-кейсы, тестирование, тестировщик по, обеспечение качества"  # noqa: B950
        else:
            context["page_title"] = "Choosing a Test Management System in 2019"
            context["page_description"] = "Many development teams sooner or later face the question of implementing specialized tools (systems) to manage the testing process on their projects. Which one should you choose? Functions overview with many screenshots."  # noqa: B950
            context["page_keywords"] = "test management, testing tools, qa management, software testing, test case management"  # noqa: B950
        return context


def redirect_old_images(request, rest_path):
    """Redirect for blog images from old static website."""
    return redirect(f"{settings.STATIC_URL}blog/{rest_path}", permanent=True)
