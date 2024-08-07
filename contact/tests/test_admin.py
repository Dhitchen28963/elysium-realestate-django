from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from contact.admin import ContactMessageAdmin
from contact.models import ContactMessage

class MockRequest:
    pass

class ContactMessageAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.admin = ContactMessageAdmin(ContactMessage, self.site)

    def test_list_display(self):
        self.assertEqual(self.admin.list_display, ('name', 'email', 'created_at'))

    def test_search_fields(self):
        self.assertEqual(self.admin.search_fields, ('name', 'email'))
