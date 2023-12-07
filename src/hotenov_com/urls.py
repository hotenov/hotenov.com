"""hotenov_com's URL configuration."""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views as flatpage_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic.base import RedirectView

from resume import views as resume_views
from website import views as website_views
from website.sitemaps import ResumeSitemap
from website.sitemaps import StaticViewSitemap


sitemaps = {
    "static": StaticViewSitemap,
    "resume": ResumeSitemap,
}


# Not translated URLs
urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        flatpage_views.flatpage,
        {"url": "/robots.txt/"},
        name="robots",
    ),
    path(
        "blog/tms-review-2019.html",
        RedirectView.as_view(url="/ru/blog/tms-review-2019/", permanent=True),
        name="old_tms-review-2019",
    ),
    path(
        "ru/blog/tms-review-2019.html",
        RedirectView.as_view(url="/ru/blog/tms-review-2019/", permanent=True),
        name="ru_tmp_old_tms-review-2019",
    ),
    path(
        "resume.html",
        RedirectView.as_view(url="/ru/resume/", permanent=True),
        name="old_resume",
    ),
    path(
        "blog/posts.html",
        RedirectView.as_view(pattern_name="website:blog", permanent=True),
        name="old_blog_list",
    ),
    path(
        "contact.html",
        RedirectView.as_view(pattern_name="website:contact", permanent=True),
        name="old_contact",
    ),
    path(
        "about.html",
        RedirectView.as_view(pattern_name="website:about", permanent=True),
        name="old_about",
    ),
    re_path(
        r"^blog/img/(?P<rest_path>.+)$",
        website_views.redirect_old_images,
        name="old_blog_images",
    ),
]


website_patterns = (
    [
        # ex: /
        path("", website_views.IndexView.as_view(), name="index"),
        path("about/", website_views.AboutView.as_view(), name="about"),
        path("contact/", website_views.ContactView.as_view(), name="contact"),
        path("blog/", website_views.OldBlogView.as_view(), name="blog"),
        path(
            "blog/tms-review-2019/",
            website_views.OldBlogPageView.as_view(),
            name="tms-review-2019",
        ),
    ],
    "website",
)

resume_patterns = (
    [
        # path("", resume_views.ResumeIndexView.as_view(), name="index"),
        path("", resume_views.ResumeDetailView.as_view(), name="index"),
        path(
            "<slug:slug>/",
            resume_views.ResumeDetailView.as_view(),
            name="detail",
        ),
    ],
    "resume",
)


urlpatterns += i18n_patterns(
    # path("", include(website_patterns, namespace="website")),
    path("", include(website_patterns)),
    # path("resume/", include(resume_patterns, namespace="resume")),
    path("resume/", include(resume_patterns)),
    prefix_default_language=False,
)


# # Without language prefix
# urlpatterns += [
#     path("", include("website.urls")),
# ]


# Serve media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
