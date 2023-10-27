from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Tag, Ingredient, Recipe
from .serializers import (
    TagSerializer,
    IngredientsSerializer,
    RecipeCreationSerializer,
    RecipeListSerializer,
    RecipeGetSerializer
)
from .permissions import IsAdminAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра списка рецептов, конкретного рецепта,
    создания рецепта"""
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsAdminAuthorOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        elif self.action == 'retrieve':
            return RecipeGetSerializer
        return RecipeCreationSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST', 'DELETE'], detail=False,
            url_path='favorite',
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk):
        pass
