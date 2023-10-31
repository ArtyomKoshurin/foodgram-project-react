from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Tag, Ingredient, Recipe, Favorites, ShoppingCart
from .serializers import (
    TagSerializer,
    IngredientsSerializer,
    RecipeCreationSerializer,
    RecipeListSerializer,
    RecipeGetSerializer
)
from .permissions import IsAdminAuthorOrReadOnly
from .filters import IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для просмотра списка рецептов, конкретного рецепта,
    создания рецепта"""
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsAdminAuthorOrReadOnly]
        elif self.action == 'list' or self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['list', 'favorite', 'shopping_cart']:
            return RecipeListSerializer
        elif self.request.method == 'GET':
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
            if not Favorites.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response('Этот рецепт еще не в списке избранного.',
                                status=status.HTTP_400_BAD_REQUEST)
            favorite = Favorites.objects.get(
                user=request.user, recipe=recipe)
            favorite.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE'], detail=False,
            url_path=r'(?P<pk>\d+)/shopping_cart',
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response('Этот рецепт уже в списке покупок.',
                                status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(data=self.get_serializer(recipe).data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                    user=request.user, recipe=recipe).exists():
                return Response(
                    'Вы не добавляли этот рецепт в список покупок.',
                    status=status.HTTP_400_BAD_REQUEST)
            shopping_cart = ShoppingCart.objects.get(
                user=request.user, recipe=recipe)
            shopping_cart.delete()
            return Response(data=self.get_serializer(recipe).data,
                            status=status.HTTP_204_NO_CONTENT)
