from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Tag, Ingredient, Recipe, Favorites
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
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'favorite':
            return RecipeListSerializer
        elif self.action == 'retrieve':
            return RecipeGetSerializer
        return RecipeCreationSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST', 'DELETE'], detail=False,
            url_path=r'(?P<pk>\d+)/favorite',
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, **kwargs):
        recipe = Recipe.objects.get(id=kwargs['pk'])
        serializer = RecipeListSerializer(recipe)
        if request.method == 'POST':
            if Favorites.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response('Этот рецепт уже в списке избранного.',
                                status=status.HTTP_400_BAD_REQUEST)
            Favorites.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = Favorites.objects.get(
                user=request.user, recipe=recipe)
            favorite.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
