from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_patch_user_data, signup, token_obtain

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/token/', token_obtain, name='token_obtain'),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/users/me/', get_patch_user_data, name='get_patch_user_data'),
    path('v1/', include(router.urls)),
]
