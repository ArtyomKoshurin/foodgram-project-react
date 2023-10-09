from django.urls import path, include, re_path

from users.views import CustomAuthToken


app_name = 'api'

urlpatterns = [
    path('', include('users.urls', namespace='users')),
    path('', include('recipes.urls', namespace='recipes')),
    path('auth/token/login/', CustomAuthToken.as_view()),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
