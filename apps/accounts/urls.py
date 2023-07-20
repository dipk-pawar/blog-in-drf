from .views import (
    UserCreateAPI,
    LoginAPIView,
    UserListAPIView,
    UserRetrieveUpdateDestroyView,
)
from django.urls import path

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"users", AccountModelView, basename="users")

urlpatterns = [
    path("register/", UserCreateAPI.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("users/", UserListAPIView.as_view(), name="users"),
    path(
        "users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="users-details"
    ),
]
