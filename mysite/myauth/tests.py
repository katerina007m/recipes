from http.client import responses
from django.test import TestCase
from django.urls import reverse
import json

# Создайте свои тесты здесь.
class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse("myauth:cookie-get"),
                                    **{'HTTP_USER_AGENT': 'Mozilla/5.0'})
        self.assertContains(response, "Cookies value")

class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse("myauth:foo-bar"),
                                   **{'HTTP_USER_AGENT': 'Mozilla/5.0'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['content-type'], 'application/json',
        )
        expected_data = {"foo": "bar", "spam": "eggs"}
        recieved_data = json.loads(response.content)
        self.assertEqual(recieved_data, expected_data)
        self.assertJSONEqual(response.content, expected_data)