from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Blog, Comment
from django.utils import timezone
import json

class BlogListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            content='This is a test blog.',
            status='published',
            created_on=timezone.now()
        )

    def test_blog_list_view(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog')

class BlogDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            content='This is a test blog.',
            status='published',
            created_on=timezone.now()
        )

    def test_blog_detail_view_get(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog')

    def test_blog_detail_view_post(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'body': 'This is a test comment.',
        }
        response = self.client.post(reverse('blog_detail', args=[self.blog.slug]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.blog, author=self.user, body='This is a test comment.').exists())

class CommentEditViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            content='This is a test blog.',
            status='published',
            created_on=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.blog,
            author=self.user,
            body='This is a test comment.',
            created_on=timezone.now(),
            approved=True,
            pending_approval=False
        )

    def test_comment_edit_view_post(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'body': 'This is an edited test comment.',
        }
        response = self.client.post(
            reverse('comment_edit', args=[self.comment.id]),
            data=json.dumps(form_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'This is an edited test comment.')
        self.assertFalse(self.comment.approved)  # The comment should be marked as not approved

class DeleteCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            content='This is a test blog.',
            status='published',
            created_on=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.blog,
            author=self.user,
            body='This is a test comment.',
            created_on=timezone.now(),
            approved=True,
            pending_approval=False
        )

    def test_delete_comment_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('comment_delete', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
