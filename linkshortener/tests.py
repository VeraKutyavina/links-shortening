import datetime
import json
from django.test import TestCase
from django.urls import reverse

from .models import Link


class LinkModelTests(TestCase):
    def test_save_link_without_short_url(self):
        # save() generate short links for instance without it

        link = Link(long_link="test")
        link.save()

        self.assertIsNotNone(link.short_link)


def create_link():
    return Link.objects.create(long_link="test")


class LinkIndexView(TestCase):
    def test_index_redirect_to_create(self):
        response = self.client.get(reverse('index'))

        self.assertRedirects(response, reverse('create'), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class LinkCreateView(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse('create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create it now!')

    def test_post_request(self):
        data = {
            'long_link': 'fiesta'
        }
        response = self.client.post(reverse('create'), data={'long_link': 'https://docs.python.org/3' })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your new short URL')


class LinkAllLinksView(TestCase):
    def test_no_links(self):
        response = self.client.get(reverse('allLinks'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No links are available.')
        self.assertQuerysetEqual(response.context['links'], [])
