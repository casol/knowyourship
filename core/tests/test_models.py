from django.test import TestCase
from django.contrib.auth.models import User

from core.models import ShipList, ShipDetails, ShipImage, ShipCoordinates


class ShipListTest(TestCase):
    """Test ShipList model."""
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.com',
                                             password='test')
        self.s = ShipList.objects.create(ship='USS Test', country='Testland',
                                         region='Testo', city='Test City',
                                         from_country='Testland', year='2017',
                                         ship_class='Tester', remarks='Just ship',
                                         slug='uss-test')

    def test_str(self):
        """test_str should return ship name."""
        self.assertEqual(self.s.ship, str(self.s))

    def test_ship_creation(self):
        """test_ship_creation() should return ship name for the ship field."""
        self.assertTrue(isinstance(self.s, ShipList))
        self.assertEqual(self.s.__str__(), self.s.ship)

    def test_ship_field(self):
        field_ship = self.s._meta.get_field('ship').verbose_name
        self.assertEqual(field_ship, 'ship')

    def test_ship_field_max_length(self):
        max_length = self.s._meta.get_field('ship').max_length
        self.assertEqual(max_length, 200)

    def test_country_field(self):
        field_country = self.s._meta.get_field('country').verbose_name
        self.assertEqual(field_country, 'country')

    def test_country_field_max_length(self):
        max_length = self.s._meta.get_field('country').max_length
        self.assertEqual(max_length, 200)

    def test_region_field(self):
        field_region = self.s._meta.get_field('region').verbose_name
        self.assertEqual(field_region, 'region')

    def test_region_field_max_length(self):
        max_length = self.s._meta.get_field('region').max_length
        self.assertEqual(max_length, 250)

    def test_city_field(self):
        field_city = self.s._meta.get_field('city').verbose_name
        self.assertEqual(field_city, 'city')

    def test_city_field_max_length(self):
        max_length = self.s._meta.get_field('city').max_length
        self.assertEqual(max_length, 250)

    def test_from_country_field(self):
        field_from_country = self.s._meta.get_field('from_country').verbose_name
        self.assertEqual(field_from_country, 'from country')

    def test_from_country_field_max_length(self):
        max_length = self.s._meta.get_field('from_country').max_length
        self.assertEqual(max_length, 200)

    def test_year_field(self):
        field_year = self.s._meta.get_field('year').verbose_name
        self.assertEqual(field_year, 'year')

    def test_year_field_max_length(self):
        max_length = self.s._meta.get_field('year').max_length
        self.assertEqual(max_length, 20)

    def test_ship_class_field(self):
        field_ship_class = self.s._meta.get_field('ship_class').verbose_name
        self.assertEqual(field_ship_class, 'ship class')

    def test_ship_class_field_max_length(self):
        max_length = self.s._meta.get_field('ship_class').max_length
        self.assertEqual(max_length, 200)

    def test_ship_type_field(self):
        field_ship_type = self.s._meta.get_field('ship_type').verbose_name
        self.assertEqual(field_ship_type, 'ship type')

    def test_ship_type_field_max_length(self):
        max_length = self.s._meta.get_field('ship_type').max_length
        self.assertEqual(max_length, 200)

    def test_remarks_field(self):
        field_remarks = self.s._meta.get_field('remarks').verbose_name
        self.assertEqual(field_remarks, 'remarks')

    def test_remarks_field_max_length(self):
        max_length = self.s._meta.get_field('remarks').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        self.assertEqual(self.s.get_absolute_url(), '/core/'+self.s.slug+'/')


class ShipDetailsTest(TestCase):
    """Test ShipDetails model."""
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.com',
                                             password='test')
        self.ship = ShipList.objects.create(ship='USS Test', country='Testland',
                                            region='Testo', city='Test City',
                                            from_country='Testland', year='2017',
                                            ship_class='Tester', remarks='Just ship')
        self.details = ShipDetails.objects.create(ship=self.ship,
                                                  content='TestTesttesttes',
                                                  remarks='cs')

    def test_ship_details_creation(self):
        """test_ship_details_creation() should return ship name."""
        self.assertTrue(isinstance(self.details, ShipDetails))
        self.assertEqual(self.details.__str__(), 'USS Test')

    def test_content_field(self):
        field_content = self.details._meta.get_field('content').verbose_name
        self.assertEqual(field_content, 'content')

    def test_remarks_field(self):
        field_remarks = self.details._meta.get_field('remarks').verbose_name
        self.assertEqual(field_remarks, 'remarks')

    def test_remarks_field_max_length(self):
        max_length = self.details._meta.get_field('remarks').max_length
        self.assertEqual(max_length, 250)


class ShipCoordinatesTest(TestCase):
    """Test ShipCoordinates model."""
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.com',
                                             password='test')
        self.ship = ShipList.objects.create(ship='USS Test', country='Testland',
                                            region='Testo', city='Test City',
                                            from_country='Testland', year='2017',
                                            ship_class='Tester', remarks='Just ship')
        self.coordinates = ShipCoordinates.objects.create(ship=self.ship,
                                                          latitude=15.2231,
                                                          longitude=-33.5542,
                                                          country='Some land')

    def test_ship_coordinates_creation(self):
        """test_ship_coordinates_creation() should return ship coordinates."""
        self.assertTrue(isinstance(self.coordinates, ShipCoordinates))
        self.assertEqual(self.coordinates.__str__(), 'lat: 15.2231, lng: -33.5542')

    def test_latitude_field(self):
        field_latitude = self.coordinates._meta.get_field('latitude').verbose_name
        self.assertEqual(field_latitude, 'latitude')

    def test_longitude_field(self):
        field_longitude = self.coordinates._meta.get_field('longitude').verbose_name
        self.assertEqual(field_longitude, 'longitude')

    def test_country_field(self):
        field_country = self.coordinates._meta.get_field('country').verbose_name
        self.assertEqual(field_country, 'country')

    def test_country_field_max_length(self):
        max_length = self.coordinates._meta.get_field('country').max_length
        self.assertEqual(max_length, 50)
