from django.test import TestCase
from django.contrib.auth.models import User

from core.models import ShipList


class ShipListTest(TestCase):
    """Test ShipList model."""
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.com',
                                             password='test')
        self.s = ShipList.objects.create(ship='USS Test', country='Testland',
                                         region='Testo', city='Test City',
                                         from_country='Testland', year='2017',
                                         ship_class='Tester', remarks='Just ship')

    def test_ship_creation(self):
        """test_ship_creation() should return ship name for ship field."""
        self.assertTrue(isinstance(self.s, ShipList))
        self.assertEqual(self.s.__str__(), self.s.ship)

    def test_ship_field(self):
        field_ship = self.s._meta.get_field('ship').verbose_name
        self.assertEqual(field_ship, 'ship')

    def test_ship_field_max_length(self):
        max_length = self.s._meta.get_field('ship').max_length
        self.assertEqual(max_length, 250)

    def test_country_field(self):
        field_country = self.s._meta.get_field('country').verbose_name
        self.assertEqual(field_country, 'country')

    def test_country_field_max_length(self):
        max_length = self.s._meta.get_field('country').max_length
        self.assertEqual(max_length, 250)

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
        self.assertEqual(max_length, 250)

    def test_year_field(self):
        field_year = self.s._meta.get_field('year').verbose_name
        self.assertEqual(field_year, 'year')

    def test_year_field_max_length(self):
        max_length = self.s._meta.get_field('year').max_length
        self.assertEqual(max_length, 250)

    def test_ship_class_field(self):
        field_ship_class = self.s._meta.get_field('ship_class').verbose_name
        self.assertEqual(field_ship_class, 'ship class')

    def test_ship_class_field_max_length(self):
        max_length = self.s._meta.get_field('ship_class').max_length
        self.assertEqual(max_length, 250)

    def test_ship_type_field(self):
        field_ship_type = self.s._meta.get_field('ship_type').verbose_name
        self.assertEqual(field_ship_type, 'ship type')

    def test_ship_type_field_max_length(self):
        max_length = self.s._meta.get_field('ship_type').max_length
        self.assertEqual(max_length, 250)

    def test_remarks_field(self):
        field_remarks = self.s._meta.get_field('remarks').verbose_name
        self.assertEqual(field_remarks, 'remarks')

    def test_remarks_field_max_length(self):
        max_length = self.s._meta.get_field('remarks').max_length
        self.assertEqual(max_length, 250)
