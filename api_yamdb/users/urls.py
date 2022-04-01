from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import signup, token_obtain, patch_get_user_data, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/token/', token_obtain, name='token_obtain'),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/users/me/', patch_get_user_data, name='patch_get_user_data'),
    path('v1/', include(router.urls)),
]
