# from django.test import override_settings
# from django.test import SimpleTestCase
# from django.test import TestCase
# from django.urls import reverse


# class MyTestSuite(TestCase):

#     def test_resume_response(self):
#         response = self.client.get(reverse('website:resume'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Открыт к предложениям.")


#     # @override_settings(ALLOWED_HOSTS=['testserver'])
#     def test_old_blog_page_redirect(self):
#         # response = self.client.get("https://testserver/blog/tms-review-2019.html", follow=True, secure=True)
#         response = self.client.get("/blog/tms-review-2019.html", follow=True, secure=True)
#         # self.assertEqual(response.status_code, 200)
#         self.assertRedirects(
#             response,
#             status_code=302,
#             target_status_code=200,
#             expected_url="/blog/tms-review-2019/",
#         )
#         # assert response.redirect_chain == [("https://example.com/blog/tms-review-2019/", 302)]
#         # assert response.redirect_chain == [("/blog/tms-review-2019/", 302)]
#         self.assertEqual(response.redirect_chain, [("/blog/tms-review-2019/", 302)])


    # def test_old_blog_page_redirect_with_protocol(self):
    #     response = self.client.get("https://example.com/blog/tms-review-2019.html", follow=True, secure=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, status_code=302, target_status_code=200, expected_url="https://example.com/blog/tms-review-2019/")


# class MyTestSuiteOverrideSettings(TestCase):

#     def test_correct_redirect(self):
#         response = self.client.get(reverse('website:resume'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Открыт к предложениям.")


# class MyTestSuiteNoDB(SimpleTestCase):

#     def test_resume_response(self):
#         response = self.client.get(reverse('website:resume'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Открыт к предложениям.")


#     def test_old_blog_page_redirect(self):
#         response = self.client.get("/blog/tms-review-2019.html", follow=True, secure=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertRedirects(response, status_code=302, target_status_code=200, expected_url="/blog/tms-review-2019/")
#         # assert response.redirect_chain == [("https://example.com/blog/tms-review-2019/", 302)]
#         # assert response.redirect_chain == [("/blog/tms-review-2019/", 302)]
#         self.assertEqual(response.redirect_chain, [("/blog/tms-review-2019/", 302)])
