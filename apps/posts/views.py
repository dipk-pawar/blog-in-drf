from rest_framework import generics
from .models import BlogPost, Comment, Like
from .serializers import BlogPostSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class AllBlogPostsAPIView(generics.ListAPIView):
    """
    API endpoint to retrieve all blog posts.

    Permissions:
    - AllowAny: This view is accessible to anyone, even without authentication.

    Serializer:
    - BlogPostSerializer: Serializes the blog post data for the response.

    Queryset:
    - BlogPost.objects.all(): Retrieves all blog post objects from the database.
    """

    permission_classes = [AllowAny]
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()


class BlogPostListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to retrieve, update, or delete a specific blog post for the authenticated user.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this view.

    Serializer:
    - BlogPostSerializer: Serializes the blog post data for the response.

    Methods:
    - get_queryset(): Returns the queryset of blog posts authored by the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        """
        Retrieve the list of blog posts authored by the authenticated user.
        """
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific blog post for the authenticated user.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this view.

    Serializer:
    - BlogPostSerializer: Serializes the blog post data for the response.

    Methods:
    - get_queryset(): Returns the queryset of blog posts authored by the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        """
        Retrieve the list of blog posts authored by the authenticated user.
        """
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class CommentsAPIView(ModelViewSet):
    """
    API endpoint to list and create comments for the authenticated user.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this view.

    Serializer:
    - CommentSerializer: Serializes and validates the request data for comment creation.

    Methods:
    - get_queryset(): Returns the queryset of comments authored by the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Retrieve the list of comments authored by the authenticated user.
        """
        user = self.request.user
        return Comment.objects.filter(author=user)


class LikeViewSet(ModelViewSet):
    """
    API endpoint to list and create likes for the authenticated user.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this view.

    Serializer:
    - LikeSerializer: Serializes and validates the request data for like creation.

    Methods:
    - get_queryset(): Returns the queryset of likes created by the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        """
        Retrieve the list of likes created by the authenticated user.
        """
        user = self.request.user
        return Like.objects.filter(user=user)
