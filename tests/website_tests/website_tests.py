"""Unit tests for website app."""
import xml.etree.ElementTree as ET
from io import BytesIO

import pytest
from pytest_django.asserts import assertContains
from pytest_django.asserts import assertRedirects


# # FIXTURES # #


@pytest.fixture
def sitemap_file_default(db, client):
    """Get sitemap XML file with default domain."""
    response = client.get("/sitemap.xml")
    return BytesIO(response.content)


@pytest.fixture
def sitemap_file_custom_domain(db, client):
    """Get sitemap XML file with custom domain."""
    from django.contrib.sites.models import Site

    default_site = Site.objects.all()[0]
    # Change default domain and its name
    default_site.domain = "custom.example.com"
    default_site.name = "custom.example.com"
    default_site.save()
    response = client.get("/sitemap.xml")
    return BytesIO(response.content)


@pytest.fixture
def find_tag_by_url(db):
    """Find <url> entry in <urlset> by URL value."""

    def find_in_sitemap(sitemap, url):
        namespaces = {
            "": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        tree = ET.parse(sitemap)
        root = tree.getroot()
        for url_tag in root.findall("url", namespaces):
            url_text = url_tag.find("loc", namespaces).text
            if url == url_text:
                return url_tag
        return None

    return find_in_sitemap


# # TESTS # #


def test_root_health_check(client):
    """Check that root path (/) is OK."""
    response = client.get("/")
    assertContains(
        response,
        "Copyright &copy;",
        status_code=200,
    )


def test_verify_views_names_for_several_simple_pages(client):
    """Verify views that served responses from several simple pages."""
    from website.views import IndexView
    from website.views import OldBlogPageView

    response = client.get("/")
    assert response.resolver_match.func.__name__ == IndexView.as_view().__name__
    blog_response = client.get("/blog/")
    # NOTE: It will be changed, when 'blog' app will be added
    assert (
        blog_response.resolver_match.func.__name__ == OldBlogPageView.as_view().__name__
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "old, new",
    [
        ("/blog/tms-review-2019.html", "/ru/blog/tms-review-2019/"),
        ("/ru/blog/tms-review-2019.html", "/ru/blog/tms-review-2019/"),
        # ("/resume.html", "/resume/"),  # move to resume tests
        ("/blog/posts.html", "/blog/"),
        ("/contact.html", "/contact/"),
        ("/about.html", "/about/"),
    ],
)
class TestRedirectsFromOldStaticPages:
    """Test suite for checking redirects for old pages."""

    def test_redirect_from_old_static_pages(self, client, old, new):
        """Check redirect for old HTML static URLs."""
        response = client.get(old, follow=True, secure=True)
        assertRedirects(
            response,
            status_code=301,
            target_status_code=200,
            expected_url=new,
        )


@pytest.mark.django_db
class TestFlatPages:
    """Test suite for checking creation and response of flat pages."""

    def test_robots_txt_status_code_404_clean_db(self, client):
        """Check that /robots.txt does not exist in new db."""
        response = client.get("/robots.txt")
        assert response.status_code == 404

    def test_robots_txt_creation(self, client):
        """Check creation of robots.txt."""
        from django.contrib.flatpages.models import FlatPage
        from django.contrib.sites.models import Site

        flat = FlatPage(
            url="/robots.txt",  # without trailing slash
            title="Robots File",
            content="User-agent: *\nDisallow: /*.xml$",
            template_name="website/flatpages/robots.txt",
        )

        # Create record in database to store its id
        flat.save()

        site = Site.objects.get(id=1)
        # requires the objects to already be saved (that's why we did flat.save())
        flat.sites.add(site)

        response = client.get("/robots.txt", follow=True, secure=True)
        assertContains(
            response,
            "User-agent: *\nDisallow: /*.xml$",
            status_code=200,
        )

    def test_robots_txt_html_escaped_response(self, client):
        """Check redirect for '/robots.txt/'."""
        from django.contrib.flatpages.models import FlatPage
        from django.contrib.sites.models import Site

        flat = FlatPage(
            url="/robots.txt/",  # Pay attention: with trail slash as well
            title="Robots File",
            content="HTML <p>content<p> of robots.txt",
            template_name="website/flatpages/robots.txt",
        )

        # Create record in database to store its id
        flat.save()

        site = Site.objects.get(id=1)
        # requires the objects to already be saved (that's why we did flat.save())
        flat.sites.add(site)
        response = client.get("/robots.txt", follow=True, secure=True)
        assertContains(
            response,
            "HTML &lt;p&gt;content&lt;p&gt; of robots.txt",
            status_code=200,
        )


@pytest.mark.django_db
class TestSitemapForSingleWebsitePages:
    """Test suite for checking sitemap.xml content.

    Generated for single (static) website pages
    """

    def test_sitemap_xml_status_code_200(self, client):
        """Check that /sitemap.xml can be retrieved."""
        response = client.get("/sitemap.xml")
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "url_path",
        [
            "about",
            "contact",
            "resume",
            "ru/about",  # RU urls as well
            "ru/contact",
            "ru/resume",
        ],
    )
    def test_sitemap_entries_for_single_pages(
        self, url_path, sitemap_file_default, find_tag_by_url
    ):
        """Check that sitemap entries exists for pages URLs."""
        from django.conf import settings

        # Get domain from the settings
        default_domain = settings.SITE_DOMAIN
        url_tag = find_tag_by_url(
            sitemap_file_default,
            f"https://{default_domain}/{url_path}/",
        )
        assert url_tag is not None

    def test_changing_default_site_domain_in_sitemap(
        self, sitemap_file_custom_domain, find_tag_by_url
    ):
        """Check that sitemap entry takes domain value from database."""
        url_tag = find_tag_by_url(
            sitemap_file_custom_domain,
            "https://custom.example.com/",
        )
        assert url_tag is not None

    @pytest.mark.custom_domain("www.example.com")
    def test_domain_according_to_site_id_setting(
        self, client, django_db_setup_with_custom_domain
    ):
        """Check that sitemap.xml is generated with updated domain for SITE_ID=1."""
        response = client.get("/sitemap.xml")
        # Intentionally without parsing XML (i.e. as plain text)
        # To have ability to use @pytest.mark.custom_domain()
        url_entry = "<url><loc>https://www.example.com/resume/</loc><changefreq>daily</changefreq><priority>0.5</priority>"  # noqa: B950
        assertContains(response, url_entry)

    @pytest.mark.parametrize(
        "url_path",
        [
            "about",
            "contact",
            "resume",
        ],
    )
    def test_sitemap_alternate_urls_for_single_pages_2(
        self, url_path, site_domain, sitemap_file_default, find_tag_by_url
    ):
        """Check that sitemap contains alternate URLs for single pages."""
        en_url = {
            "rel": "alternate",
            "hreflang": "en",
            "href": f"https://{site_domain}/{url_path}/",
        }
        ru_url = {
            "rel": "alternate",
            "hreflang": "ru",
            "href": f"https://{site_domain}/ru/{url_path}/",
        }
        expected_links = [en_url, ru_url]

        url_tag = find_tag_by_url(
            sitemap_file_default,
            en_url["href"],
        )
        assert url_tag is not None

        namespaces = {
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        # Find all child <xhtml:link/> tags in 'xml.etree.ElementTree' instance
        for alternate in url_tag.findall("xhtml:link", namespaces):
            # Look <xhtml:link/> attributes in list of expected links
            assert dict(alternate.attrib) in expected_links

    @pytest.mark.parametrize(
        "url_path, lang",
        [
            ("", "en"),  # home page
            ("about/", "en"),
            ("contact/", "en"),
            ("blog/tms-review-2019/", "en"),
            ("ru/", "ru"),  # RU home page
            ("ru/about/", "ru"),
            ("ru/contact/", "ru"),
            ("ru/blog/tms-review-2019/", "ru"),
        ],
    )
    def test_html_language_for_single_pages(self, client, url_path, lang):
        """Check that language code in <html> tag is correct."""
        response = client.get(f"/{url_path}")
        html_lang = f'<html lang="{lang}"'  # noqa: B950
        assertContains(response, html_lang)


@pytest.mark.django_db
class TestTMSReview2019Page:
    """Test suite for checking 'TMS Review 2019' page.

    Meta tags (with OG tags) and main tags in <head> for two languages EN, RU.
    """

    def test_tms2019_available_on_new_URL(self, client):
        """Check that page 'TMS Review 2019' is available on new URL."""
        response = client.get("/blog/tms-review-2019/")
        assert response.status_code == 200

    def test_tms2019_og_site_name_and_type(self, client):
        """Check OG meta tags for 'site_name' and 'type' properties."""
        site_name = '<meta property="og:site_name" content="hotenov.com" />'
        og_type = '<meta property="og:type" content="article" />'
        response = client.get("/ru/blog/tms-review-2019/", secure=True)
        assertContains(response, site_name)
        assertContains(response, og_type)

    def test_tms2019_og_image_url(self, client, settings):
        """Check a generation of URL for image in Open Graph meta tags."""
        settings.STATIC_URL = "st/"
        og_image = '<meta property="og:image" content="https://testserver/st/blog/sc/sc-post-0001-2.png"'  # noqa: B950
        response = client.get("/blog/tms-review-2019/", secure=True)
        assertContains(response, og_image)

    def test_tms2019_og_image_properties(self, client):
        """Check Open Graph meta tags for image properties."""
        width = '<meta property="og:image:width" content="600" />'
        height = '<meta property="og:image:height" content="314" />'
        image_type = '<meta property="og:image:type" content="image/png" />'
        response = client.get("/blog/tms-review-2019/", secure=True)
        assertContains(response, width)
        assertContains(response, height)
        assertContains(response, image_type)

    def test_tms2019_alternate_urls(self, client):
        """Check alternate URLs for 'TMS Review 2019' page."""
        ru = '<link rel="alternate" hreflang="ru" href="https://testserver/ru/blog/tms-review-2019/">'  # noqa: B950
        en = '<link rel="alternate" hreflang="en" href="https://testserver/blog/tms-review-2019/">'  # noqa: B950
        default = '<link rel="alternate" hreflang="x-default" href="https://testserver/" />'  # noqa: B950
        response = client.get("/blog/tms-review-2019/", secure=True)
        assertContains(response, ru)
        assertContains(response, en)
        assertContains(response, default)

    def test_tms2019_en_title_description_keywords(self, client):
        """Check title, description and keywords meta properties for EN language."""
        title = "<title>Choosing a Test Management System in 2019&#20;▮hotenov</title>"  # noqa: B950
        description = '<meta name="description" content="Many development teams sooner or later face the question of implementing specialized tools (systems) to manage the testing process on their projects. Which one should you choose? Functions overview with many screenshots." />'  # noqa: B950
        keywords = '<meta name="keywords" content="test management, testing tools, qa management, software testing, test case management" />'  # noqa: B950
        response = client.get("/blog/tms-review-2019/")
        assertContains(response, title)
        assertContains(response, description)
        assertContains(response, keywords)

    def test_tms2019_ru_title_description_keywords(self, client):
        """Check title, description and keywords meta properties for RU language."""
        title = "<title>Обзор систем управления тестированием в 2019, платные и бесплатные&#20;▮hotenov</title>"  # noqa: B950
        description = '<meta name="description" content="Для многих команд разработки рано или поздно встает вопрос о внедрении специализированных инструментов (систем) для управления процессом тестирования в своих проектах. Какой же из них выбрать? Рассмотрим 11 таких систем." />'  # noqa: B950
        keywords = '<meta name="keywords" content="система управления, тестовые сценарии, тест-кейсы, тестирование, тестировщик по, обеспечение качества" />'  # noqa: B950
        response = client.get("/ru/blog/tms-review-2019/")
        assertContains(response, title)
        assertContains(response, description)
        assertContains(response, keywords)

    def test_tms2019_en_og_main_properties(self, client):
        """Check Open Graph meta tags for main properties (EN)."""
        og_url = '<meta property="og:url" content="https://testserver/blog/tms-review-2019/" />'  # noqa: B950
        og_title = '<meta property="og:title" content="Choosing a Test Management System in 2019" />'  # noqa: B950
        og_description = '<meta property="og:description" content="Many development teams sooner or later face the question of implementing specialized tools (systems) to manage the testing process on their projects. Which one should you choose? Functions overview with many screenshots." />'  # noqa: B950
        og_image_alt = '<meta property="og:image:alt" content="Article title over a footage of Matrix movie in the background (choosing a capsule (red or blue) on open palms)." />'  # noqa: B950
        response = client.get("/blog/tms-review-2019/", secure=True)
        assertContains(response, og_url)
        assertContains(response, og_title)
        assertContains(response, og_description)
        assertContains(response, og_image_alt)

    def test_tms2019_ru_og_main_properties(self, client):
        """Check Open Graph meta tags for main properties (RU)."""
        og_url = '<meta property="og:url" content="https://testserver/ru/blog/tms-review-2019/" />'  # noqa: B950
        og_title = '<meta property="og:title" content="Выбор системы управления тестированием в 2019" />'  # noqa: B950
        og_description = '<meta property="og:description" content="Для многих команд разработки рано или поздно встает вопрос о внедрении специализированных инструментов для управления процессом тестирования в своих проектах. Какой же из них выбрать? Рассмотрим 11 таких систем." />'  # noqa: B950
        og_image_alt = '<meta property="og:image:alt" content="Название статьи на фоне кадра из фильма Матрица (выбор таблетки на открытых ладонях: красная или синяя)" />'  # noqa: B950
        response = client.get("/ru/blog/tms-review-2019/", secure=True)
        assertContains(response, og_url)
        assertContains(response, og_title)
        assertContains(response, og_description)
        assertContains(response, og_image_alt)

    def test_tms2019_twitter_card_image_url(self, client, settings):
        """Check a generation of URL for image in Twitter meta tags."""
        settings.STATIC_URL = "stat/"
        og_image = '<meta name="twitter:image" content="https://testserver/stat/blog/sc/sc-post-0001-1.png"'  # noqa: B950
        response = client.get("/ru/blog/tms-review-2019/", secure=True)
        assertContains(response, og_image)

    def test_tms2019_sitemap_alternate_urls(self, client, site_domain):
        """Check that sitemap contains alternate URLs for 'TMS Review 2019' page."""
        response = client.get("/sitemap.xml")
        ru_url = f'<xhtml:link rel="alternate" hreflang="ru" href="https://{site_domain}/ru/blog/tms-review-2019/"/>'  # noqa: B950
        en_url = f'<xhtml:link rel="alternate" hreflang="en" href="https://{site_domain}/blog/tms-review-2019/"/>'  # noqa: B950
        assertContains(response, ru_url)
        assertContains(response, en_url)


def test_meta_og_default_image_properties(client, settings):
    """Check Open Graph meta tags for default image properties."""
    settings.STATIC_URL = "static/"
    og_image = '<meta property="og:image" content="https://testserver/static/assets/img/default-og-preview-1200x628.jpg"'  # noqa: B950
    width = '<meta property="og:image:width" content="1200" />'
    height = '<meta property="og:image:height" content="628" />'
    image_type = '<meta property="og:image:type" content="image/jpeg" />'
    response = client.get("/blog/tms-review-2019/", secure=True)
    assertContains(response, og_image)
    assertContains(response, width)
    assertContains(response, height)
    assertContains(response, image_type)
    response_main = client.get("/ru/", secure=True)
    assertContains(response_main, og_image)
    assertContains(response_main, width)
