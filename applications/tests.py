from django.test import TestCase
from django.urls import resolve

from applications.views import HomePage


class TestHomePageView(TestCase):

    def test_resolve_to_home_page(self):
        # resolve root path
        found = resolve('/')

        # check function name is equal
        self.assertEqual(found.func.__name__, HomePage.as_view().__name__)

    def test_get_home_page(self):
        # get url localhost:8000/
        response = self.client.get('/')

        # check which template is used
        self.assertTemplateUsed(response, 'home.html')

        # check response status is equal to 200
        self.assertEqual(response.status_code, 200)