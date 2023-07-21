from rest_framework.response import Response
from rest_framework import generics
from .serializers import AccountSerializer, LoginSerializers, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from blog.jwt_custom_token import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .permissions import SuperuserOnly, SuperuserORLoggedinUser
from rest_framework.exceptions import PermissionDenied


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


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, SuperuserOnly]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, SuperuserORLoggedinUser]
    serializer_class = UserSerializer

    def get_object(self):
        # Get the logged-in user
        user = self.request.user

        # Check if the URL PK matches the logged-in user's PK
        url_pk = self.kwargs["pk"]
        if user.pk != url_pk:
            # If the URL PK is not the same as the logged-in user's PK, raise PermissionDenied
            raise PermissionDenied("You do not have permission to access this user.")

        return user
