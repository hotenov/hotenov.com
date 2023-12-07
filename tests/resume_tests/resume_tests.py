"""Unit tests for resume app."""
import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains
from pytest_django.asserts import assertNotContains
from pytest_django.asserts import assertRedirects

from resume.models import Resume


# @pytest.mark.django_db()
# def test_certain_string_when_no_published_resume(client):
#     """Check response when list of resume is empty."""
#     response = client.get(reverse("resume:index"))
#     assertContains(
#         response,
#         "No resume has been published yet. Try later...",
#         status_code=200,
#     )
@pytest.mark.django_db()
def test_404_status_when_no_resume_on_index_url(client):
    """Check response when no resume on 'index' url path."""
    response = client.get(reverse("resume:index"))
    assert response.status_code == 404
    response = client.get("/ru/resume/")
    assert response.status_code == 404


@pytest.fixture
def resume_factory(db):
    """Factory fixture for creation of Resume object."""

    def create_resume(
        role,
        person_name,
        slug="test-resume-slug",
    ):
        """Create Resume object."""
        resume = Resume.objects.create(
            role=role,
            person_name=person_name,
            slug=slug,
        )
        return resume

    return create_resume


@pytest.fixture
def resume_A(db, resume_factory):
    """Create resume A object."""
    resume_A = resume_factory(
        role="Test Developer Position",
        person_name="John SmithInTest",
    )
    return resume_A


@pytest.fixture
def resume_B_published(db, resume_factory):
    """Create resume B object (published)."""
    resume_B = resume_factory(
        role="Test Developer Position",
        person_name="John SmithInTest",
        slug="case-b-published",
    )
    resume_B.is_published = True
    resume_B.save()
    return resume_B


def test_should_create_published_resume_A(resume_B_published):
    """Check creation of published resume in db."""
    assert resume_B_published.slug == "case-b-published"
    assert resume_B_published.is_published


def test_sitemap_not_contain_unpublished_resume(site_domain, client, resume_A):
    """Check that sitemap does not generate entries for unpublished resume."""
    resume_url = resume_A.get_absolute_url()
    url_entry = f"<loc>https://{site_domain}{resume_url}</loc>"
    response = client.get("/sitemap.xml")
    assertNotContains(response, url_entry)


def test_sitemap_contains_published_resume(site_domain, client, resume_B_published):
    """Check that sitemap entries auto generate entry for published resume."""
    resume_url = resume_B_published.get_absolute_url()
    response = client.get("/sitemap.xml")
    url_entry = f"<loc>https://{site_domain}{resume_url}</loc>"
    assertContains(response, url_entry)


def test_sitemap_resume_last_modification_date(client, resume_B_published):
    """Check lastmod attribute for published resume."""
    update_date = resume_B_published.updated_at.strftime("%Y-%m-%d")
    response = client.get("/sitemap.xml")
    lastmod_attr = f"<lastmod>{update_date}</lastmod>"
    assertContains(response, lastmod_attr)


def test_sitemap_resume_has_fixed_changefreq_and_priority(
    site_domain, client, resume_B_published
):
    """Check resume url has fixed (hardcoded) change frequency and priority."""
    resume_url = resume_B_published.get_absolute_url()
    loc_attr = f"<loc>https://{site_domain}{resume_url}</loc>"

    update_date = resume_B_published.updated_at.strftime("%Y-%m-%d")
    lastmod_attr = f"<lastmod>{update_date}</lastmod>"

    change_frequency = "monthly"
    changefreq_attr = f"<changefreq>{change_frequency}</changefreq>"

    priority = "0.7"
    priority_attr = f"<priority>{priority}</priority>"

    resume_entry = loc_attr + lastmod_attr + changefreq_attr + priority_attr

    response = client.get("/sitemap.xml")
    assertContains(response, resume_entry)


@pytest.mark.parametrize(
    "url_path, lang",
    [
        ("resume/", "en"),
        ("ru/resume/", "ru"),
    ],
)
def test_html_language_for_resume_index_url(
    client,
    url_path,
    lang,
    resume_B_published,
):
    """Check that language code in <html> tag is correct."""
    resume_B_published.display_on_main = True
    resume_B_published.save()
    response = client.get(f"/{url_path}")
    html_lang = f'<html lang="{lang}"'
    assertContains(response, html_lang)


def test_redirect_from_old_static_resume_page(client, resume_B_published):
    """Check redirect for old HTML static '/resume.html' page."""
    resume_B_published.display_on_main = True
    resume_B_published.save()
    old = "/resume.html"
    new = "/ru/resume/"
    response = client.get(old, follow=True, secure=True)
    assertRedirects(
        response,
        status_code=301,
        target_status_code=200,
        expected_url=new,
    )
