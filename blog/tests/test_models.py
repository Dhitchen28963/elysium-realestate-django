from django.test import TestCase
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.models import ContentType
from blog.models import Post, Comment, PostImage

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_post(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post.',
            status='draft'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.author.username, 'testuser')
        self.assertEqual(post.status, 'draft')
        self.assertEqual(str(post), 'Test Post')

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post.',
            status='published'
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a test comment.',
            approved=True,
            content_type=ContentType.objects.get_for_model(Post),
            object_id=self.post.id,
        )
        self.assertEqual(comment.post.title, 'Test Post')
        self.assertEqual(comment.author.username, 'testuser')
        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertTrue(comment.approved)
        self.assertEqual(str(comment), f'Comment by testuser on Test Post')

class PostImageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post.',
            status='published'
        )

    def test_create_post_image(self):
        post_image = PostImage.objects.create(
            post=self.post,
            image='test_image.jpg'
        )
        self.assertEqual(post_image.post.title, 'Test Post')
        self.assertEqual(post_image.image, 'test_image.jpg')
        self.assertEqual(str(post_image), 'Image for Test Post')
