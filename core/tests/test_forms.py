from django.test import TestCase
from core.forms import SearchFrom
from django import forms


class SearchFormTest(TestCase):

    def test_form_renders(self):
        """test_form_renders() tests input attributes render by HTML."""
        form = SearchFrom()
        self.assertIn('placeholder="Search"', form.as_p())
        self.assertIn('name="query"', form.as_p())
        self.assertIn('id="id_query"', form.as_p())
        self.assertIn('type="text"', form.as_p())

    def test_search_form_field_text_input(self):
        """test_search_form_field_text_input() should return text input."""
        form = SearchFrom(initial={'query': 'USS First'},)
        self.assertEqual(form['query'].value(), 'USS First')

    def test_search_form_validation(self):
        """test_search_form_validation() checks form with is_valid() method."""
        form_data = {'query': 'something'}
        form = SearchFrom(data=form_data)
        self.assertTrue(form.is_valid())
