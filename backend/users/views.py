from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .pagination import UsersPagination, RecipePagination
from .models import CustomUser, Subscription
from .serializers import (
    UserRegistrationSerializer,
    UserInfoSerializer,
    TokenSerializer,
    NewPasswordSerializer,
    UserRecipesSerializer,
)


class MixinsForUserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                           mixins.ListModelMixin, mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    pass


class UserViewSet(MixinsForUserViewSet):
    """Вьюсет для регистрации пользователя, просмотра списка пользователей
    и просмотра отдельного пользователя."""
    queryset = CustomUser.objects.all()
    pagination_class = UsersPagination
    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserInfoSerializer
        elif self.request.method == 'GET' or self.action in [
            'subscribe',
            'subscriptions'
        ]:
            return UserRecipesSerializer
        return UserRegistrationSerializer

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def my_profile(self, request):
        """Метод, позволяющий посмотреть свой профиль."""
        serializer = UserInfoSerializer(request.user,
                                        context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='set_password',
            permission_classes=(permissions.IsAuthenticated,))
    def change_password(self, request):
        """Метод, позволяющий сменить пароль."""
        user = CustomUser.objects.get(username=request.user.username)
        serializer = NewPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if serializer.data['current_password'] == request.user.password:
                user.password = serializer.data['new_password']
                user.save(update_fields=["password"])
                return Response('Пароль успешно изменен.',
                                status=status.HTTP_204_NO_CONTENT)

        return Response('Неверный текущий пароль.',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', 'DELETE'], detail=False,
            url_path=r'(?P<pk>\d+)/subscribe',
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(CustomUser, id=kwargs['pk'])
        serializer = UserRecipesSerializer(author,
                                           context={'request': request})

        if request.method == 'POST':
            if Subscription.objects.filter(
                    user=request.user, author=author).exists():
                return Response('Вы уже подписаны на этого пользователя.',
                                status=status.HTTP_400_BAD_REQUEST)
            elif request.user == author:
                return Response('Нельзя подписаться на самого себя.',
                                status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(user=request.user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Subscription.objects.filter(
                    user=request.user, author=author).exists():
                return Response('Вы не подписаны на этого пользователя.',
                                status=status.HTTP_400_BAD_REQUEST)
            subscription = Subscription.objects.get(
                user=request.user, author=author)
            subscription.delete()
            return Response(serializer.data,
                            status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False,
            url_path='subscriptions',
            permission_classes=(permissions.IsAuthenticated,),
            pagination_class=RecipePagination)
    def subscriptions(self, request):
        authors = CustomUser.objects.filter(
            recipe_author__user=request.user).prefetch_related('recipes')
        page = self.paginate_queryset(authors)

        if page:
            serializer = UserRecipesSerializer(
                page, many=True,
                context={'request': request})

            return self.get_paginated_response(serializer.data)
        serializer = UserRecipesSerializer(authors, many=True,
                                           context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    """Кастомный вью-класс для получения токена по username-email."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data,
                                     context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                CustomUser,
                email=serializer.data.get('email')
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'auth_token': token.key,
            })

        return Response('Неверный пароль или email.',
                        status=status.HTTP_400_BAD_REQUEST)
