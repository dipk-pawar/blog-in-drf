from django.shortcuts import render
from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BlogPostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
