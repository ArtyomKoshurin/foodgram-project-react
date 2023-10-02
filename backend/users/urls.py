from django.urls import path
from .views import UserRegistrationViewSet

app_name = 'users'

urlpatterns = [
    path('',
         UserRegistrationViewSet.as_view({'get': 'list', 'post': 'create'}))
]
