from django.urls import include, path
from .views import signup, token_obtain, patch_user_data

app_name = 'users'


urlpatterns = [
    path('auth/token/', token_obtain, name='token_obtain'),
    path('auth/signup/', signup, name='signup'),
    # path('users/me/', patch_user_data, name='patch_user_data'),
]
