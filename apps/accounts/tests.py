from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


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


class LoginAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("login")

        # Create a test user
        self.user_data = {
            "email": "test@example.com",
            "first_name": "Dipak",
            "last_name": "Pawar",
            "password": "testpassword",
            "is_active": True,
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_login_success(self):
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.url, data=login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the access and refresh tokens
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_login_invalid_credentials(self):
        invalid_login_data = {
            "email": self.user_data["email"],
            "password": "invalidpassword",
        }
        response = self.client.post(self.url, data=invalid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the error message for invalid credentials
        self.assertIn("errors", response.data)
        self.assertIn("non_field_errors", response.data["errors"])

    def test_login_missing_email_or_password(self):
        # Test case for missing email or password fields
        missing_email_data = {"password": "testpassword"}
        response = self.client.post(self.url, data=missing_email_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the error message for missing email field
        self.assertIn("email", response.data)

        missing_password_data = {"email": "test@example.com"}
        response = self.client.post(self.url, data=missing_password_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the error message for missing password field
        self.assertIn("password", response.data)


class UserListAPIViewTest(APITestCase):
    def setUp(self):
        # Create a test superuser
        self.super_user = User.objects.create_superuser(
            email="superuser@example.com",
            password="testpassword",
            first_name="Dipak",
            last_name="Pawar",
        )

        # Create a regular user
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpassword",
            first_name="Dip",
            last_name="Pawar",
        )

        self.url = reverse("users")

    def test_superuser_access(self):
        # Log in the superuser
        self.client.force_authenticate(user=self.super_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the serialized user data
        self.assertEqual(len(response.data), User.objects.count())

    def test_regular_user_access(self):
        # Log in the regular user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        # Do not log in any user
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        # Create a test superuser
        self.superuser = User.objects.create_superuser(
            email="superuser@example.com",
            password="testpassword",
            first_name="Dipak",
            last_name="Pawar",
        )

        # Create a regular user
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpassword",
            first_name="Dip",
            last_name="Pawar",
            is_active=True,
        )

        self.url = "users-details"

    def test_superuser_access(self):
        # Log in the superuser
        self.client.force_authenticate(user=self.superuser)

        # Make a request to retrieve, update, or delete the superuser's own data
        url = reverse(self.url, kwargs={"pk": self.superuser.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_update(self):
        # Log in the superuser
        self.client.force_authenticate(user=self.superuser)

        # Make a request to update the superuser's own data
        new_data = {
            "first_name": "Updated Dipak",
            "last_name": "Updated Pawar",
        }
        url = reverse(self.url, kwargs={"pk": self.superuser.pk})
        response = self.client.put(url, data=new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user data has been updated
        updated_user = User.objects.get(pk=self.superuser.pk)
        self.assertEqual(updated_user.first_name, new_data["first_name"])
        self.assertEqual(updated_user.last_name, new_data["last_name"])

    def test_superuser_delete(self):
        # Log in the superuser
        self.client.force_authenticate(user=self.superuser)

        # Make a request to delete the superuser's own data
        url = reverse(self.url, kwargs={"pk": self.superuser.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the user has been deleted from the database
        self.assertFalse(User.objects.filter(pk=self.superuser.pk).exists())

    def test_regular_user_access_own_data(self):
        # Log in the regular user
        self.client.force_authenticate(user=self.user)

        # Make a request to retrieve, update, or delete the regular user's own data
        url = reverse(self.url, kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_update(self):
        # Log in the regular user
        self.client.force_authenticate(user=self.user)

        # Make a request to update the regular user's own data
        new_data = {
            "first_name": "Updated Dip",
            "last_name": "Updated Pawar",
        }
        url = reverse(self.url, kwargs={"pk": self.user.pk})
        response = self.client.put(url, data=new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user data has been updated
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, new_data["first_name"])
        self.assertEqual(updated_user.last_name, new_data["last_name"])

    def test_regular_user_delete(self):
        # Log in the regular user
        self.client.force_authenticate(user=self.user)

        # Make a request to delete the regular user's own data
        url = reverse(self.url, kwargs={"pk": self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the user has been deleted from the database
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_regular_user_access_other_user_data(self):
        # Log in the regular user
        self.client.force_authenticate(user=self.user)

        # Attempt to access the superuser's data (which should be denied)
        url = reverse(self.url, kwargs={"pk": self.superuser.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        # Do not log in any user
        self.client.force_authenticate(user=None)

        # Attempt to access a user's data without authentication (which should be denied)
        url = reverse(self.url, kwargs={"pk": self.superuser.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
