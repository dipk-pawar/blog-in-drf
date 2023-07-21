from django.urls import path
from .views import (
    BlogPostListCreateView,
    BlogPostRetrieveUpdateDestroyView,
    AllBlogPostsAPIView,
    CommentsAPIView,
    LikeViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"comments", CommentsAPIView, basename="comments")
router.register(r"likes", LikeViewSet, basename="likes")

urlpatterns = [
    path("all-posts/", AllBlogPostsAPIView.as_view(), name="all-blogpost-list"),
    path("", BlogPostListCreateView.as_view(), name="blogpost-list-create"),
    path(
        "<int:pk>/",
        BlogPostRetrieveUpdateDestroyView.as_view(),
        name="blogpost-detail",
    ),
] + router.urls
