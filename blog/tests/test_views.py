from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment
from django.utils import timezone

class PostListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post.',
            status='published',
            created_on=timezone.now()
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

class PostDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post.',
            status='published',
            created_on=timezone.now()
        )

    def test_post_detail_view_get(self):
        response = self.client.get(reverse('blog_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view_post(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'body': 'This is a test comment.',
        }
        response = self.client.post(reverse('blog_detail', args=[self.post.slug]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.user, body='This is a test comment.').exists())

class CommentEditViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post.',
            status='published',
            created_on=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a test comment.',
            created_on=timezone.now(),
            approved=True,
            content_type=self.post.get_content_type(),
            object_id=self.post.id,
        )

    def test_comment_edit_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('comment_edit', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test comment.')

    def test_comment_edit_view_post(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'body': 'This is an edited test comment.',
        }
        response = self.client.post(reverse('comment_edit', args=[self.comment.id]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'This is an edited test comment.')

class DeleteCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post.',
            status='published',
            created_on=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a test comment.',
            created_on=timezone.now(),
            approved=True,
            content_type=self.post.get_content_type(),
            object_id=self.post.id,
        )

    def test_delete_comment_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('comment_delete', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
