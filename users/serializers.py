from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50, validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="username already taken."
            )
        ],
    )
    email = serializers.EmailField(max_length=127, validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already registered."
            )
        ],
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(max_length=50, write_only=True)

    def create(self, validated_data: dict) -> User:

        return User.objects.create(**validated_data)

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)
