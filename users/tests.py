from django.test import TestCase
from django.contrib.auth import get_user_model

"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

This class utilizes Django testing framework along with Coverage.
Is is used to test the Users model specifcally along with validation testing of the model enties.

"""

class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'robert', 'firstname', 'digital', 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.user_name, 'robert')
        self.assertEqual(super_user.first_name, 'firstname')
        self.assertEqual(super_user.company_name, 'digital')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "robert")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', user_name='username1', first_name='first_name', last_name='digital', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', user_name='username1', first_name='first_name', last_name='digital', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='username1', first_name='first_name', last_name='digital',  password='password', is_superuser=True)

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'robert', 'firstname', 'digital', 'password')
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.user_name, 'robert')
        self.assertEqual(user.first_name, 'firstname')
        self.assertEqual(user.last_name, 'digital')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', user_name='a', first_name='first_name', last_name='digital', password='password')
