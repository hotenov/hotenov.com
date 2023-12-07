"""Website URLconf."""
# from django.contrib.sitemaps.views import sitemap
# from django.urls import path
# from django.urls import reverse_lazy
# from django.views.generic.base import RedirectView

# from . import views
# from .sitemaps import ResumeSitemap
# from .sitemaps import StaticViewSitemap


# app_name = "website"

# sitemaps = {
#     "static": StaticViewSitemap,
#     "resume": ResumeSitemap,
# }

# urlpatterns = [
#     # ex: /
#     path("", views.IndexView.as_view(), name="index"),
#     path("about/", views.AboutView.as_view(), name="about"),
#     path("contact/", views.ContactView.as_view(), name="contact"),
#     # path("resume/", views.ResumeView.as_view(), name="resume"),
#     # path("resume.html", views.ResumeView.as_view(), name="old_resume"),
#     path("blog/", views.OldBlogView.as_view(), name="blog"),
#     path(
#         "sitemap.xml",
#         sitemap,
#         {"sitemaps": sitemaps},
#         name="django.contrib.sitemaps.views.sitemap",
#     ),
#     path(
#         "blog/tms-review-2019/",
#         views.OldBlogPageView.as_view(),
#         name="tms-review-2019",
#     ),
#     path(
#         "blog/tms-review-2019.html",
#         # RedirectView.as_view(url="/blog/tms-review-2019/"),
#         RedirectView.as_view(url=reverse_lazy("website:tms-review-2019")),
#         name="old_tms-review-2019",
#     ),
#     path(
#         "resume.html",
#         # RedirectView.as_view(url="/resume/"),
#         RedirectView.as_view(url=reverse_lazy("resume:index")),
#         name="old_resume",
#     ),
#     path(
#         "blog/posts.html",
#         # RedirectView.as_view(url="/blog/"),
#         RedirectView.as_view(url=reverse_lazy("website:blog")),
#         name="old_blog_list",
#     ),
#     path(
#         "contact.html",
#         # RedirectView.as_view(url="/contact/"),
#         RedirectView.as_view(url=reverse_lazy("website:contact")),
#         name="old_contact",
#     ),
#     path(
#         "about.html",
#         # RedirectView.as_view(url="/about/"),
#         RedirectView.as_view(url=reverse_lazy("website:about")),
#         name="old_about",
#     ),
# ]
