from rest_framework import serializers
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email_address(email):
    try:
        validate_email(email)
    except ValidationError:
        raise serializers.ValidationError(_("Email is not valid"), code="authorization")
    return email


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """Serializer for user login."""
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                _('Must include "email" and "password".'), code="authorization"
            )

        email = validate_email_address(email)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("password", None)
        representation.pop("is_active", None)
        representation.pop("is_staff", None)
        return representation


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
        read_only_fields = ["id", "email"]
