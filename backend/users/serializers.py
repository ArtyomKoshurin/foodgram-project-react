import re

from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'password')

    def validate_username(self, value):
        """Проверяет, что в имени не содержатся запрещенные символы и что
        оно не занято."""
        error_list = []
        username = value
        for symbol in username:
            if not re.search(r'^[\w.@+-]+$', symbol):
                error_list.append(symbol)
        if error_list:
            raise serializers.ValidationError(
                f'Символы {"".join(error_list)} запрещены!'
            )
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"Имя {value} уже занято!")
        return value

    def validate_email(self, value):
        """Проверяет, что указанный адрес почты не занят."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "На этот адрес эл. почты уже зарегистрирован аккаунт!"
            )
        return value


class UserInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра профилей пользователей."""
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""
    password = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = CustomUser
        fields = ('password', 'email')
