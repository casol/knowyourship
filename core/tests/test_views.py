from django.test import TestCase
from django.test.client import RequestFactory

from core.models import ShipList, ShipDetails
from core.views import ship_search, get_ship


class RequestTest(TestCase):

    def setUp(self):
        # Every test need access to the request factory.
        self.factory = RequestFactory()

        self.ship = ShipList.objects.create(ship='USS Test', country='Testland',
                                            region='Testo', city='Test City',
                                            from_country='Testland', year='2017',
                                            ship_class='Tester', remarks='Just ship')

    def test_base_view_without_client(self):
        """test_base_view_without_client() sending a request to the
        view mapped to '/' and asserting that the response is returned as expected.
        """
        request = self.factory.get('/')
        response = ship_search(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "KNOW YOUR SHIP!")

    def test_ajax_autocomplete_search(self):
        """test_ajax_autocomplete_search() sending a request to
        a view where an AJAX call is expected.
        """
        request = self.factory.get('/get_ship/?term=uss',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = get_ship(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")
