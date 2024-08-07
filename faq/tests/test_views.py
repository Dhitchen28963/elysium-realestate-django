from django.test import TestCase, Client
from django.urls import reverse
from faq.models import FAQ, Comment
from django.contrib.auth.models import User
from django.utils import timezone
import json

class FAQViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.faq = FAQ.objects.create(
            title='Test FAQ', 
            slug='test-faq', 
            author=self.user, 
            content='Test content', 
            status='published'
        )

    def test_faq_list_view(self):
        response = self.client.get(reverse('faq_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test FAQ')

    def test_faq_detail_view(self):
        response = self.client.get(reverse('faq_detail', args=[self.faq.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test content')

    def test_add_comment_view(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'body': 'This is a test comment.',
        }
        response = self.client.post(reverse('faq_detail', args=[self.faq.slug]), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.faq, author=self.user, body='This is a test comment.').exists())

    def test_edit_comment_view(self):
        comment = Comment.objects.create(post=self.faq, author=self.user, body='This is a test comment.')
        self.client.login(username='testuser', password='testpass')
        form_data = {
            'body': 'This is an edited test comment.',
        }
        response = self.client.post(reverse('faq_comment_edit', args=[comment.id]), data=json.dumps(form_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.body, 'This is an edited test comment.')

    def test_delete_comment_view(self):
        comment = Comment.objects.create(post=self.faq, author=self.user, body='This is a test comment.')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('faq_comment_delete', args=[comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
