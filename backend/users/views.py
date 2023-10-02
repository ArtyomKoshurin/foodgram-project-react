from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserInfoSerializer


class UserRegistrationViewSet(viewsets.ModelViewSet):
    """Вьюсет для регистрации пользователя, просмотра списка пользователей
    и просмотра отдельного пользователя."""
    queryset = CustomUser.objects.all()
    pagination_class = PageNumberPagination

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

    @action(methods=['GET'], detail=True, url_path='me')
    def my_profile(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
