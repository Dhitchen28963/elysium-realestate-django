from django.contrib import admin
from django.test import TestCase
from blog.admin import PostAdmin, CommentAdmin, PostImageInline
from blog.models import Post, Comment, PostImage
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
        self.assertEqual(self.post_admin.list_display, ('title', 'slug', 'author', 'created_on', 'status'))

    def test_post_admin_search_fields(self):
        self.assertEqual(self.post_admin.search_fields, ['title', 'content'])

    def test_post_admin_prepopulated_fields(self):
        self.assertEqual(self.post_admin.prepopulated_fields, {'slug': ('title',)})

    def test_post_admin_inlines(self):
        self.assertEqual(len(self.post_admin.inlines), 1)
        self.assertEqual(self.post_admin.inlines[0], PostImageInline)

class TestCommentAdmin(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.comment_admin = CommentAdmin(Comment, self.site)

    def test_comment_admin_list_display(self):
        self.assertEqual(self.comment_admin.list_display, ('author', 'content_object', 'created_on', 'approved'))

    def test_comment_admin_list_filter(self):
        self.assertEqual(self.comment_admin.list_filter, ('approved', 'created_on'))

    def test_comment_admin_search_fields(self):
        self.assertEqual(self.comment_admin.search_fields, ('author__username', 'body'))

class TestPostImageInline(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.post_image_inline = PostImageInline(PostImage, self.site)

    def test_post_image_inline_model(self):
        self.assertEqual(self.post_image_inline.model, PostImage)

    def test_post_image_inline_extra(self):
        self.assertEqual(self.post_image_inline.extra, 1)
