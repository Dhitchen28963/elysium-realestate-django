from django.contrib import admin
from django.test import TestCase
from property_guides.admin import PostAdmin, CategoryAdmin, PropertyImageInline
from property_guides.models import Post, Category, PropertyImage
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin.sites import AdminSite


class MockRequest:
    pass


class TestPostAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.post_admin = PostAdmin(Post, self.site)

    def test_post_admin_inheritance(self):
        self.assertTrue(issubclass(PostAdmin, SummernoteModelAdmin))

    def test_post_admin_list_display(self):
        self.assertEqual(self.post_admin.list_display, ('title', 'category', 'created_on', 'updated_on'))

    def test_post_admin_search_fields(self):
        self.assertEqual(self.post_admin.search_fields, ('title', 'content'))

    def test_post_admin_prepopulated_fields(self):
        self.assertEqual(self.post_admin.prepopulated_fields, {'slug': ('title',)})

    def test_post_admin_fields(self):
        self.assertEqual(self.post_admin.fields, ('title', 'slug', 'category', 'featured_image', 'content'))

    def test_post_admin_inlines(self):
        self.assertEqual(len(self.post_admin.inlines), 1)
        self.assertEqual(self.post_admin.inlines[0], PropertyImageInline)


class TestCategoryAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.category_admin = CategoryAdmin(Category, self.site)

    def test_category_admin_list_display(self):
        self.assertEqual(self.category_admin.list_display, ('name',))

    def test_category_admin_search_fields(self):
        self.assertEqual(self.category_admin.search_fields, ('name',))


class TestPropertyImageInline(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.property_image_inline = PropertyImageInline(PropertyImage, self.site)

    def test_property_image_inline_model(self):
        self.assertEqual(self.property_image_inline.model, PropertyImage)

    def test_property_image_inline_extra(self):
        self.assertEqual(self.property_image_inline.extra, 1)
