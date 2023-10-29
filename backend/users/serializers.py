import re

from rest_framework import serializers

from .models import CustomUser, Subscription
from recipes.serializers import RecipeListSerializer


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
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(
            author=obj, user=request.user).exists()


class UserShortInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого отображения пользователя на главной странице
    рецептов."""
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name')


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""
    password = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = CustomUser
        fields = ('password', 'email')


class NewPasswordSerializer(serializers.Serializer):
    """Сериализатор для получения нового пароля."""
    new_password = serializers.CharField(max_length=150, required=True)
    current_password = serializers.CharField(max_length=150, required=True)


class UserRecipesSerializer(UserInfoSerializer):
    """Сериализатор для просмотра профиля пользователя с его рецептами."""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = UserInfoSerializer.Meta.fields + (
            'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipe_limit = request.query_params.get('recipes_limit')
        queryset = obj.recipes.all()
        if recipe_limit:
            queryset = queryset[:int(recipe_limit)]

        recipes_to_show = RecipeListSerializer(
            queryset, many=True)
        return recipes_to_show.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
