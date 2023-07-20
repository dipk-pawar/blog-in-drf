from rest_framework import serializers
from .models import BlogPost, Comment
from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BlogPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = "__all__"

    def to_representation(self, instance):
        blog_post = super().to_representation(instance)
        user = User.objects.get(id=instance.author.id)
        blog_post["author"] = UserSerializer(instance=user).data
        return blog_post
