from django.urls import include, path
from .views import signup, token_obtain

app_name = 'users'


urlpatterns = [
    path('auth/token/', token_obtain, name='token_obtain'),
    path('auth/signup/', signup, name='signup'),
]
