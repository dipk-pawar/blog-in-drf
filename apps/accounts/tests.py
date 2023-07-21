from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateAPITest(APITestCase):
    def setUp(self):
        self.url = reverse("register")

        # Test data for creating a new user
        self.valid_user_data = {
            "email": "test@example.com",
            "first_name": "Dipak",
            "last_name": "Pawar",
            "password": "testpassword",
        }

    def test_create_user_success(self):
        response = self.client.post(self.url, data=self.valid_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the user was created with the correct data
        self.assertTrue(
            User.objects.filter(email=self.valid_user_data["email"]).exists()
        )
        user = User.objects.get(email=self.valid_user_data["email"])
        self.assertEqual(user.first_name, self.valid_user_data["first_name"])
        self.assertEqual(user.last_name, self.valid_user_data["last_name"])
        self.assertTrue(user.check_password(self.valid_user_data["password"]))

        # Check if sensitive data like "password", "is_active", "is_staff" are not returned in the response
        self.assertNotIn("password", response.data)
        self.assertNotIn("is_active", response.data)
        self.assertNotIn("is_staff", response.data)

    def test_create_user_missing_email_password(self):
        # Test case for missing "email" and "password" fields
        invalid_data = {
            "first_name": "Dipak",
            "last_name": "Pawar",
        }
        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the error message for missing "email" and "password"
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_create_user_invalid_email(self):
        # Test case for an invalid email address
        invalid_data = {
            "email": "invalid_email",
            "first_name": "Dipak",
            "last_name": "Pawar",
            "password": "testpassword",
        }
        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the error message for an invalid email address
        self.assertIn("email", response.data)
