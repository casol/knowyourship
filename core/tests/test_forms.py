from django.test import TestCase
from core.forms import CommentForm, ContactForm, SearchForm
from core.models import ShipList
from django.core.mail import  send_mail, BadHeaderError


class SearchFormTest(TestCase):
    def setUp(self):
        self.ship = ShipList.objects.create(ship='USS Test', country='Testland',
                                            region='Testo', city='Test City',
                                            from_country='Testland', year='2017',
                                            ship_class='Tester', remarks='Just ship',
                                            slug='uss-test')

    def test_form_renders(self):
        """test_form_renders() tests input attributes render by HTML."""
        form = SearchForm()
        self.assertIn('class="form-control form-control-lg"', form.as_p())

    def test_search_form_field_text_input(self):
        """test_search_form_field_text_input() should return text input."""
        form = SearchForm(initial={'query': 'USS First'},)
        self.assertEqual(form['query'].value(), 'USS First')

    def test_search_form_validation(self):
        """test_search_form_validation() checks form with is_valid() method."""
        form_data = {'query': 'something'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CommentFormTest(TestCase):

    def test_form_renders_item_input(self):
        """test_form_renders() tests input attributes render by HTML."""
        form = CommentForm()
        # test Bootstrap CSS classes
        self.assertIn('class="form-control"', form.as_p())

    def test_comment_valid(self):
        """test_comment_form_validation() checks form with is_valid() method."""
        form = CommentForm(data={'name': 'Tester',
                                 'email': 'test@test.com',
                                 'body': 'testoo'})
        self.assertTrue(form.is_valid())

    def test_comment_invalid(self):
        """test_comment_form_validation() checks form with is_valid() method."""
        form = CommentForm(data={'name': '', 'email': '',
                                 'body': 'testoo'})
        self.assertFalse(form.is_valid())

    def test_comment_form_field_name_input(self):
        form = CommentForm(initial={'name': 'Tester'})
        self.assertEqual(form['name'].value(), 'Tester')

    def test_comment_form_field_email_input(self):
        form = CommentForm(initial={'email': 'test@test.com'})
        self.assertEqual(form['email'].value(), 'test@test.com')

    def test_comment_form_field_text_input(self):
        form = CommentForm(initial={'body': 'Test test test.'})
        self.assertEqual(form['body'].value(), 'Test test test.')


class ContactFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        """test_form_renders() tests input attributes render by HTML."""
        form = ContactForm()
        # test Bootstrap CSS classes
        self.assertIn('class="form-control"', form.as_p())

    def test_contact_valid(self):
        """test_contact_form_validation() checks form with is_valid() method."""
        form = ContactForm(data={'name': 'Tester',
                                 'email': 'test@test.com',
                                 'subject': 'testoo',
                                 'message': 'Test test test.'})
        self.assertTrue(form.is_valid())

    def test_contact_invalid(self):
        """test_contact_form_validation() checks form with is_valid() method."""
        form = ContactForm(data={'name': 'Tester',
                                 'email': '',
                                 'subject': 'testoo',
                                 'message': 'Test test test.'})

        self.assertFalse(form.is_valid())

    def test_contact_form_field_name_input(self):
        form = ContactForm(initial={'name': 'Tester'})
        self.assertEqual(form['name'].value(), 'Tester')

    def test_contact_form_field_email_input(self):
        form = ContactForm(initial={'email': 'test@test.com'})
        self.assertEqual(form['email'].value(), 'test@test.com')

    def test_contact_form_field_subject_input(self):
        form = ContactForm(initial={'subject': 'Test'})
        self.assertEqual(form['subject'].value(), 'Test')

    def test_contact_form_field_message_input(self):
        form = ContactForm(initial={'message': 'Teste test test.'})
        self.assertEqual(form['message'].value(), 'Teste test test.')

    def test_header(self):
        """test_header should return true if BadHeaderError occur."""
        error_occured = False
        try:
            send_mail('Header\nInjection', 'Here is the message.', 'from@example.com',
                      ['to@example.com'], fail_silently=False)
        except BadHeaderError:
            error_occured = True
        self.assertTrue(error_occured)
