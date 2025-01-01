from django.test import TestCase
from django.urls import reverse

class SimpleTests(TestCase):
    def test_main_page(self):
        response = self.client.get(reverse('base'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_page(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
