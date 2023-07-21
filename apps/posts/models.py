from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    author = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    likes = models.ManyToManyField(
        "accounts.User", through="posts.Like", related_name="liked_posts"
    )
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        "posts.BlogPost", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    content = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"


class Like(models.Model):
    post = models.ForeignKey("posts.BlogPost", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.first_name} on {self.post.title}"
