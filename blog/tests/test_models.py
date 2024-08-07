from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Blog, Comment, BlogImage

class BlogModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_blog(self):
        blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            content='This is a test blog.',
            status='draft'
        )
        self.assertEqual(blog.title, 'Test Blog')
        self.assertEqual(blog.slug, 'test-blog')
        self.assertEqual(blog.author.username, 'testuser')
        self.assertEqual(blog.status, 'draft')
        self.assertEqual(str(blog), 'Test Blog')

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            content='This is a test blog.',
            status='published'
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.blog,
            author=self.user,
            body='This is a test comment.',
            approved=True,
        )
        self.assertEqual(comment.post.title, 'Test Blog')
        self.assertEqual(comment.author.username, 'testuser')
        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertTrue(comment.approved)
        self.assertEqual(str(comment), f'Comment by {comment.author} on {comment.post}')

class BlogImageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            author=self.user,
            content='This is a test blog.',
            status='published'
        )

    def test_create_blog_image(self):
        blog_image = BlogImage.objects.create(
            post=self.blog,
            image='test_image.jpg'
        )
        self.assertEqual(blog_image.post.title, 'Test Blog')
        self.assertEqual(blog_image.image, 'test_image.jpg')
        self.assertEqual(str(blog_image), 'Image for Test Blog')
