from .views import UserCreateAPI, LoginAPIView
from django.urls import path

urlpatterns = [
    path("register/", UserCreateAPI.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
]
