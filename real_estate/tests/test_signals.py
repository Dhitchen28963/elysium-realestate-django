from django.test import TestCase
from django.contrib.auth.models import User
from real_estate.models import Profile

class UserSignalTests(TestCase):

    def test_create_user_profile_signal(self):
        """
        Test that a Profile is created when a new User is created.
        """
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        # Check if Profile is created
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists, "Profile should be created when a new user is created")

    def test_save_user_profile_signal(self):
        """
        Test that the Profile is saved when the User is saved.
        """
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        # Modify the user to trigger the save signal
        user.email = 'newemail@example.com'
        user.save()
        
        # Retrieve the profile and check if it was saved
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.email, 'newemail@example.com', "Profile should be updated when the user is updated")
