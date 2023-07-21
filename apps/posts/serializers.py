from rest_framework import serializers
from .models import BlogPost, Comment, Like
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
        if instance.author:
            user = User.objects.get(id=instance.author.id)
            blog_post["author"] = UserSerializer(instance=user).data
        else:
            blog_post["author"] = {}
        blog_post["likes"] = len(instance.likes.all())
        return blog_post


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["user"]

    def create(self, validated_data):
        # Automatically set the user to the authenticated user
        user = self.context["request"].user
        return Like.objects.create(user=user, **validated_data)
