from .views import (
    UserCreateAPI,
    LoginAPIView,
    UserListAPIView,
    UserRetrieveUpdateDestroyView,
    VerifyUser,
)
from django.urls import path

urlpatterns = [
    path("register/", UserCreateAPI.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("users/", UserListAPIView.as_view(), name="users"),
    path(
        "users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="users-details"
    ),
    path(
        "verify-account/<str:uid>/",
        VerifyUser.as_view(),
        name="verify-user",
    ),
]
