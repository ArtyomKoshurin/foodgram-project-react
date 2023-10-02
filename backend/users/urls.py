from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserRegistrationViewSet

app_name = 'users'

router_api_v1 = DefaultRouter()

router_api_v1.register('users', UserRegistrationViewSet, basename='users')

urlpatterns = [
    path('', include(router_api_v1.urls))
]
