from django.urls import include, path
from .views import MyTokenObtainPairView, signUp

app_name = 'users'


urlpatterns = [
    path('auth/token/', MyTokenObtainPairView.as_view(),
         name='my_token_obtain_pair'),
    path('auth/signup/', signUp, name='signUp'),
]
