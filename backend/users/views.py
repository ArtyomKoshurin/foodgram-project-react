from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserInfoSerializer,
    TokenSerializer
)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    """Вьюсет для регистрации пользователя, просмотра списка пользователей
    и просмотра отдельного пользователя."""
    queryset = CustomUser.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserInfoSerializer
        return UserRegistrationSerializer

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        queryset = get_object_or_404(CustomUser, id=pk)
        serializer = UserInfoSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def my_profile(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    """Вью-класс для получения токена по username-email."""
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