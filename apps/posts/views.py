from rest_framework import generics
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class AllBlogPostsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()


class BlogPostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class CommentsAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user)
