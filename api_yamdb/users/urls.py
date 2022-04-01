from django.urls import include, path
from .views import signup, token_obtain, patch_user_data

app_name = 'users'


urlpatterns = [
    path('v1/auth/token/', token_obtain, name='token_obtain'),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/users/me/', patch_user_data, name='patch_user_data'),
]
