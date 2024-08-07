from django.contrib import admin
from django.test import TestCase
from blog.admin import BlogAdmin, CommentAdmin, BlogImageInline
from blog.models import Blog, Comment, BlogImage
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin.sites import AdminSite

class MockRequest:
    pass

class TestBlogAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.blog_admin = BlogAdmin(Blog, self.site)

    def test_blog_admin_inheritance(self):
        self.assertTrue(issubclass(BlogAdmin, SummernoteModelAdmin))

    def test_blog_admin_list_display(self):
        self.assertEqual(self.blog_admin.list_display, ('title', 'slug', 'author', 'created_on', 'status'))

    def test_blog_admin_search_fields(self):
        self.assertEqual(self.blog_admin.search_fields, ['title', 'content'])

    def test_blog_admin_prepopulated_fields(self):
        self.assertEqual(self.blog_admin.prepopulated_fields, {'slug': ('title',)})

    def test_blog_admin_inlines(self):
        self.assertEqual(len(self.blog_admin.inlines), 1)
        self.assertEqual(self.blog_admin.inlines[0], BlogImageInline)

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

class TestBlogImageInline(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.blog_image_inline = BlogImageInline(BlogImage, self.site)

    def test_blog_image_inline_model(self):
        self.assertEqual(self.blog_image_inline.model, BlogImage)

    def test_blog_image_inline_extra(self):
        self.assertEqual(self.blog_image_inline.extra, 1)
