from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from faq.models import FAQ, Comment
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType


class FAQListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        FAQ.objects.create(
            title='Test FAQ',
            slug='test-faq',
            author=self.user,
            content='This is a test FAQ.',
            status='published',
            created_on=timezone.now()
        )

    def test_faq_list_view(self):
        response = self.client.get(reverse('faq_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test FAQ')


class FAQDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.faq = FAQ.objects.create(
            title='Test FAQ',
            slug='test-faq',
            author=self.user,
            content='This is a test FAQ.',
            status='published',
            created_on=timezone.now()
        )

    def test_faq_detail_view_get(self):
        response = self.client.get(reverse('faq_detail', args=[self.faq.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test FAQ')

    def test_faq_detail_view_post(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'body': 'This is a test comment.',
        }
        response = self.client.post(reverse('faq_detail', args=[self.faq.slug]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.faq, author=self.user, body='This is a test comment.').exists())


class FAQCommentEditViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.faq = FAQ.objects.create(
            title='Test FAQ',
            slug='test-faq',
            author=self.user,
            content='This is a test FAQ.',
            status='published',
            created_on=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.faq,
            author=self.user,
            body='This is a test comment.',
            created_on=timezone.now(),
            approved=True,
            content_type=ContentType.objects.get_for_model(FAQ),
            object_id=self.faq.id,
        )

    def test_faq_comment_edit_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('faq_comment_edit', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test comment.')

    def test_faq_comment_edit_view_post(self):
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'body': 'This is an edited test comment.',
        }
        response = self.client.post(reverse('faq_comment_edit', args=[self.comment.id]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'This is an edited test comment.')


class DeleteFAQCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.faq = FAQ.objects.create(
            title='Test FAQ',
            slug='test-faq',
            author=self.user,
            content='This is a test FAQ.',
            status='published',
            created_on=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.faq,
            author=self.user,
            body='This is a test comment.',
            created_on=timezone.now(),
            approved=True,
            content_type=ContentType.objects.get_for_model(FAQ),
            object_id=self.faq.id,
        )

    def test_delete_faq_comment_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('faq_comment_delete', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
