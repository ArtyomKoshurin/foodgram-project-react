from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tag, Ingredient, Recipe
from .serializers import (
    TagSerializer,
    IngredientsSerializer,
    RecipeCreationSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreationSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
