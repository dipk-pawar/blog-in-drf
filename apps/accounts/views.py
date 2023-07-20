from rest_framework.response import Response
from rest_framework import generics
from .serializers import AccountSerializer, LoginSerializers
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from blog.jwt_custom_token import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class UserCreateAPI(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"errors": {"non_field_errors": ["Email or password is not valid"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokens = get_tokens_for_user(user=user)
        return Response(
            {"tokens": tokens, "message": "Login successfully"},
            status=status.HTTP_200_OK,
        )
