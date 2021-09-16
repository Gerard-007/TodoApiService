from rest_framework.test import APITestCase

from authentication.models import User


class TestModel(APITestCase):
    def test_create_user(self):
        user=User.objects.create_user("Gerard", "gerard@gmail.com", "pass=123")
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'gerard@gmail.com')

    def test_create_super_user(self):
        user=User.objects.create_superuser("Gerard", "gerard@gmail.com", "pass=123")
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'gerard@gmail.com')

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="", email="gerard@gmail.com", password="pass=123")
        self.assertRaisesMessage(ValueError, 'The given username must be set')

    def test_raises_error_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(username="", email="gerard@gmail.com", password="pass=123")

    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="Gerard", email="", password="pass=123")
        self.assertRaisesMessage(ValueError, 'The given email must be set')

    def test_raises_error_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(username="Gerard", email="", password="pass=123")

    def create_superuser_with_is_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username="Gerard", email="gerard@gmail.com", password="pass=123", is_superuser=False)

    def create_superuser_with_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username="Gerard", email="gerard@gmail.com", password="pass=123", is_staff=False)
