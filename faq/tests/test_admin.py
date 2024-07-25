from django.contrib import admin
from django.test import TestCase
from faq.admin import FAQAdmin, CommentAdmin, FAQImageInline
from faq.models import FAQ, Comment, FAQImage
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin.sites import AdminSite

class MockRequest:
    pass

class TestFAQAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.faq_admin = FAQAdmin(FAQ, self.site)

    def test_faq_admin_inheritance(self):
        self.assertTrue(issubclass(FAQAdmin, SummernoteModelAdmin))

    def test_faq_admin_list_display(self):
        self.assertEqual(self.faq_admin.list_display, ('title', 'slug', 'author', 'created_on', 'status'))

    def test_faq_admin_search_fields(self):
        self.assertEqual(self.faq_admin.search_fields, ['title', 'content'])

    def test_faq_admin_prepopulated_fields(self):
        self.assertEqual(self.faq_admin.prepopulated_fields, {'slug': ('title',)})

    def test_faq_admin_inlines(self):
        self.assertEqual(len(self.faq_admin.inlines), 1)
        self.assertEqual(self.faq_admin.inlines[0], FAQImageInline)


class TestCommentAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.comment_admin = CommentAdmin(Comment, self.site)

    def test_comment_admin_list_display(self):
        self.assertEqual(self.comment_admin.list_display, ('author', 'post', 'created_on', 'approved'))

    def test_comment_admin_list_filter(self):
        self.assertEqual(self.comment_admin.list_filter, ('approved', 'created_on'))

    def test_comment_admin_search_fields(self):
        self.assertEqual(self.comment_admin.search_fields, ['author', 'body'])

    def test_comment_admin_approve_comments_action(self):
        self.assertIn('approve_comments', self.comment_admin.actions)


class TestFAQImageInline(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.faq_image_inline = FAQImageInline(FAQImage, self.site)

    def test_faq_image_inline_model(self):
        self.assertEqual(self.faq_image_inline.model, FAQImage)

    def test_faq_image_inline_extra(self):
        self.assertEqual(self.faq_image_inline.extra, 1)
