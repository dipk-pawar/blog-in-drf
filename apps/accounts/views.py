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
    """
    API endpoint to create a new user.

    Permissions:
    - AllowAny: This view is accessible to anyone, even without authentication.

    Serializer:
    - AccountSerializer: Serializes and validates the request data for creating a new user.
    """

    permission_classes = [AllowAny]
    serializer_class = AccountSerializer


class LoginAPIView(APIView):
    """
    API endpoint for user login.

    Request method: POST

    Serializer:
    - LoginSerializers: Serializes and validates the request data for user login.

    Returns:
    - On successful login, returns a JSON response with user tokens and a success message.
    - On unsuccessful login, returns a JSON response with error messages.
    """

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
    """
    API endpoint to list all users.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this view.
    - SuperuserOnly: Only superusers can access this view.

    Serializer:
    - UserSerializer: Serializes the user data for the response.

    Queryset:
    - User.objects.all(): Retrieves all user objects from the database.
    """

    permission_classes = [IsAuthenticated, SuperuserOnly]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a user.

    Permissions:
    - IsAuthenticated: Only authenticated users can access this view.
    - SuperuserORLoggedinUser: Either the user is a superuser or the user's own profile.

    Serializer:
    - UserSerializer: Serializes the user data for the response.

    Returns:
    - On successful retrieval, returns a JSON response with the user's data.
    - On successful update, returns a JSON response with the updated user's data.
    - On successful deletion, returns a JSON response with a success message.

    Raises:
    - PermissionDenied: If the URL PK (user's primary key) does not match the logged-in user's PK,
      it means the user is trying to access someone else's profile, and PermissionDenied is raised.
    """

    permission_classes = [IsAuthenticated, SuperuserORLoggedinUser]
    serializer_class = UserSerializer

    def get_object(self):
        """
        Retrieve the user object for the currently authenticated user.

        Returns:
        - The user object for the currently authenticated user.
        """

        # Get the logged-in user
        user = self.request.user

        # Check if the URL PK matches the logged-in user's PK
        url_pk = self.kwargs["pk"]
        if user.pk != url_pk:
            # If the URL PK is not the same as the logged-in user's PK, raise PermissionDenied
            raise PermissionDenied("You do not have permission to access this user.")

        return user
