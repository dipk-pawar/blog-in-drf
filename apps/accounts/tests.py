from django.test import TestCase
from django.urls import reverse
from .models import User


# Create your tests here.
# Tests that a user can be created with valid input data
class CreateUserTestCase(TestCase):
    def test_create_user_valid_input(self):
        data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Test1234",
        }
        url = reverse("register")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    # Tests that a user can be created with a password containing special characters
    def test_create_user_special_characters_password(self):
        data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Test@1234",
        }
        url = reverse("register")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    # Tests that a user can be created with a password containing numbers
    def test_create_user_numbers_password(self):
        data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Test1234",
        }
        url = reverse("register")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    # Tests that a user can be created with a password containing uppercase and lowercase letters
    def test_create_user_uppercase_lowercase_password(self):
        data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Test1234",
        }
        url = reverse("register")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    # Tests that a user cannot be created with an existing email
    def test_create_user_existing_email(self):
        User.objects.create_user(
            email="test@test.com",
            first_name="Existing",
            last_name="User",
            password="Test1234",
        )
        data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Test1234",
        }
        url = reverse("register")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    # Tests that a user cannot be created with an invalid email
    def test_create_user_invalid_email(self):
        data = {
            "email": "invalid_email",
            "first_name": "Test",
            "last_name": "User",
            "password": "Test1234",
        }
        url = reverse("register")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
