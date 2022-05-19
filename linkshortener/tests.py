from django.test import TestCase
from django.urls import reverse

from .models import Link


# MODELS TESTS


class LinkModelTests(TestCase):
    def test_save_link_without_short_url(self):
        link = Link(long_link="test")
        link.save()

        self.assertIsNotNone(link.short_link)


# VIEWS TESTS


def create_link():
    return Link.objects.create(long_link=reverse("allLinks"))


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
        url = 'https://docs.python.org/3'
        data = {
            'long_link': url
        }
        response = self.client.post(reverse('create'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your new short URL')
        self.assertContains(response, url)

    def test_post_with_invalid_url(self):
        url = 'invalid-url'
        data = {
            'long_link': url
        }
        response = self.client.post(reverse('create'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create it now!')


class LinkRedirectView(TestCase):
    def test_redirect_to_url(self):
        link = create_link()

        response = self.client.get(reverse('redirect', kwargs={"short_link": link.short_link}))

        self.assertRedirects(response, link.long_link, status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_redirect_with_invalid_link(self):
        response = self.client.get(reverse('redirect', kwargs={"short_link": "test"}))

        self.assertEqual(response.status_code, 404)


class LinkAllLinksView(TestCase):
    def test_no_links(self):
        response = self.client.get(reverse('allLinks'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No links are available.')
        self.assertQuerysetEqual(response.context['links'], [])

    def test_contain_link(self):
        link = create_link()
        response = self.client.get(reverse('allLinks'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, link.short_link)
        self.assertQuerysetEqual(response.context['links'], [link])


class LinkRemoveView(TestCase):
    def test_no_links(self):
        remove_link = create_link()
        response = self.client.post(reverse('remove', kwargs={"link_id": remove_link.id}))
        after_response = self.client.get(reverse('redirect', kwargs={"short_link": remove_link.short_link}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(after_response.status_code, 404)

    def test_not_exist_id(self):
        response = self.client.post(reverse('remove', kwargs={"link_id": 12345}))

        self.assertEqual(response.status_code, 404)