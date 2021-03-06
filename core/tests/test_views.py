from django.test import TestCase
from django.test.client import RequestFactory
from django.test import Client
from core.models import ShipList, ShipDetails, Comment
from core.views import ship_search, get_ship, contact, about, ship_detail, ship_ranking
from django.core.urlresolvers import reverse


class RequestTest(TestCase):

    def setUp(self):
        # Every test need access to the request factory.
        # RequestFactory returns a request
        self.factory = RequestFactory()

        self.ship = ShipList.objects.create(ship='USS Test', country='Testland',
                                            region='Testo', city='Test City',
                                            from_country='Testland', year='2017',
                                            ship_class='Tester', remarks='Just ship',
                                            slug='uss-test')

    def test_base_view(self):
        """test_base_view() sending a request to the
        view mapped to '/' and asserting that the response is returned as expected.
        """
        # Create an instance of a GET request
        request = self.factory.get('/')
        # Test ship_search() as if it were deployed at example.com/
        response = ship_search(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Know Your Ship")

    def test_ajax_autocomplete_search(self):
        """test_ajax_autocomplete_search() sending a request to
        a view where an AJAX call is expected.
        """
        request = self.factory.get('/get_ship/?term=Testland',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = get_ship(request)
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        """test_contact_view() sending a request to the
        view mapped to '/contact' and asserting that the response is returned as expected.
        """
        # Create an instance of a GET request
        request = self.factory.get('/contact')
        # Test contact() as if it were deployed at example.com/contact
        response = contact(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you have any questions?")

    def test_about_view(self):
        """test_about_view() sending a request to the
        view mapped to '/about' and asserting that the response is returned as expected.
        """
        # Create an instance of a GET request
        request = self.factory.get('/about')
        # Test about() as if it were deployed at example.com/about
        response = about(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "about")

    def test_ship_ranking_view(self):
        """test_ship_ranking_view() sending a request to the
        view mapped to '/ranking' and asserting that the response is returned as expected.
        """
        # Create an instance of a GET request
        request = self.factory.get('/ranking')
        # Test about() as if it were deployed at example.com/ranking
        response = ship_ranking(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ranking")

    def test_ship_detail_view(self):
        """test_ship_detail_view() sending a request to the
        view mapped to '/ship-slug' and asserting that the response is returned as expected.
        """
        # Create an instance of a GET request
        # Get ship absolute url
        request = self.factory.get(self.ship.get_absolute_url())
        # Test ship_detail() as if it were deployed at example.com/ship-slug
        response = ship_detail(request, self.ship.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")

    def test_ship_search_view_get_request(self):
        """test_contact_view_post_request() sending a GET request with data."""
        # create the request
        data = {'query': 'Test'}
        request = self.factory.get(reverse('core:ship_search'), data)
        # get the response
        response = ship_search(request)
        self.assertEqual(response.status_code, 200)


class ViewTest(TestCase):

    def setUp(self):
        # Every test needs a Client
        self.client = Client()
        self.ship = ShipList.objects.create(ship='USS Test', country='Testland',
                                            region='Testo', city='Test City',
                                            from_country='Testland', year='2017',
                                            ship_class='Tester', remarks='Just ship',
                                            slug='uss-test')

    def test_search_view(self):
        # client returns a response (request-response cycle)
        response = self.client.get(reverse('core:ship_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/search.html')

    def test_contact_view(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_ship_ranking_view(self):
        response = self.client.get(reverse('core:ship_ranking'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['most_viewed']), 1)
        self.assertTemplateUsed(response, 'core/ranking.html')

    def test_about_view(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_ship_details_view(self):
        response = self.client.get(self.ship.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains 1 ship
        self.assertEqual(response.context['ship'].ship, 'USS Test')
        self.assertTemplateUsed(response, 'core/portfolio.html')

    def test_contact_view_post_request(self):
        """test_contact_view_post_request() sending a POST request with data."""
        # create the request
        data = {'name': 'Tes Tester',
                'email': 'test@test.com',
                'subject': 'Test, Test test',
                'message': 'TEATEASTAET'}
        response = self.client.post(reverse('core:contact'), data)
        #
        message = list(response.context['messages'])
        self.assertEqual(len(message), 1)

        self.assertEqual(response.status_code, 200)

    def test_ship_details_comments_view_post_request(self):
        """test_ship_details_comments_view_post_request()
        sending a POST request with data.
        """
        # create the request
        data = {'name': 'Tes Tester',
                'email': 'test@test.com',
                'body': 'Test, Test test'}
        # get the response
        response = self.client.post(self.ship.get_absolute_url(), data)
        self.assertEqual(response.status_code, 302)
