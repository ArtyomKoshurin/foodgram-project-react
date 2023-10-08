from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tag, Ingredient
from .serializers import (
    TagSerializer,
    IngredientsSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)
