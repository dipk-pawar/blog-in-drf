from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import BlogPost
from apps.accounts.models import User


class AllBlogPostsAPIViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Dipak",
            last_name="Pawar",
        )

        # Create test blog posts
        self.blog_post_1 = BlogPost.objects.create(
            title="Test Post 1",
            content="This is the content of Test Post 1",
            author=self.user,
        )
        self.blog_post_2 = BlogPost.objects.create(
            title="Test Post 2",
            content="This is the content of Test Post 2",
            author=self.user,
        )

        self.url = reverse("all-blogpost-list")

    def test_get_all_blog_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the serialized blog posts
        self.assertEqual(len(response.data), BlogPost.objects.count())
        self.assertEqual(response.data[0]["title"], self.blog_post_1.title)
        self.assertEqual(response.data[0]["content"], self.blog_post_1.content)
        self.assertEqual(
            response.data[0]["author"]["email"], self.blog_post_1.author.email
        )

        self.assertEqual(response.data[1]["title"], self.blog_post_2.title)
        self.assertEqual(response.data[1]["content"], self.blog_post_2.content)
        self.assertEqual(
            response.data[1]["author"]["email"], self.blog_post_2.author.email
        )


class BlogPostListCreateViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Dipak",
            last_name="Pawar",
        )

        # Create some test blog posts for the user
        self.blog_post_1 = BlogPost.objects.create(
            title="Test Post 1",
            content="This is the content of Test Post 1",
            author=self.user,
        )
        self.blog_post_2 = BlogPost.objects.create(
            title="Test Post 2",
            content="This is the content of Test Post 2",
            author=self.user,
        )

        # URL for the BlogPostListCreateView
        self.url = reverse("blogpost-list-create")

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_get_blog_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the serialized blog posts for the authenticated user
        self.assertEqual(len(response.data), 2)

        # Check if the data in the response matches the data of the created blog posts
        self.assertEqual(response.data[0]["title"], self.blog_post_1.title)
        self.assertEqual(response.data[0]["content"], self.blog_post_1.content)

        self.assertEqual(response.data[1]["title"], self.blog_post_2.title)
        self.assertEqual(response.data[1]["content"], self.blog_post_2.content)

    def test_create_blog_post(self):
        new_blog_post_data = {
            "title": "New Blog Post",
            "content": "This is the content of the new blog post.",
        }
        response = self.client.post(self.url, data=new_blog_post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the blog post was created with the correct data
        self.assertEqual(BlogPost.objects.count(), 3)
        new_blog_post = BlogPost.objects.get(title=new_blog_post_data["title"])
        self.assertEqual(new_blog_post.content, new_blog_post_data["content"])
        self.assertEqual(new_blog_post.author, self.user)


class BlogPostRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Dipak",
            last_name="Pawar",
        )

        # Create a test blog post for the user
        self.blog_post = BlogPost.objects.create(
            title="Test Post",
            content="This is the content of the test blog post.",
            author=self.user,
        )

        # URL for the BlogPostRetrieveUpdateDestroyView
        self.url = reverse("blogpost-detail", kwargs={"pk": self.blog_post.pk})

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_get_blog_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the serialized blog post
        self.assertEqual(response.data["title"], self.blog_post.title)
        self.assertEqual(response.data["content"], self.blog_post.content)
        self.assertEqual(response.data["author"]["id"], self.blog_post.author.pk)

    def test_update_blog_post(self):
        updated_data = {
            "title": "Updated Blog Post",
            "content": "This is the updated content of the blog post.",
        }
        response = self.client.put(self.url, data=updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the blog post was updated with the correct data
        updated_blog_post = BlogPost.objects.get(pk=self.blog_post.pk)
        self.assertEqual(updated_blog_post.title, updated_data["title"])
        self.assertEqual(updated_blog_post.content, updated_data["content"])

    def test_delete_blog_post(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the blog post was deleted from the database
        self.assertFalse(BlogPost.objects.filter(pk=self.blog_post.pk).exists())

    def test_unauthenticated_access(self):
        # Unauthenticate the user
        self.client.force_authenticate(user=None)

        # Try to access the API without authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to update the blog post without authentication
        response = self.client.put(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to delete the blog post without authentication
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_access(self):
        # Create another user
        other_user = User.objects.create_user(
            email="otheruser@example.com",
            password="testpassword",
            first_name="Dip",
            last_name="Pawar",
        )

        # Authenticate the other user
        self.client.force_authenticate(user=other_user)

        # Try to access the API for the blog post created by the first user (should be denied)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to update the blog post created by the first user (should be denied)
        response = self.client.put(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete the blog post created by the first user (should be denied)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
