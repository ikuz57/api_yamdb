import random

from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import CustomUserSerializer, CustomUserSerializerShort
from .models import ADMIN
from .utils import send_email_with_code

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    confirmation_code = str(random.randint(10000, 20000))
    serializer = CustomUserSerializerShort(data=request.data)
    if serializer.is_valid():
        serializer.save(confirmation_code=confirmation_code)
        send_email_with_code(serializer.data['email'], confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain(request):
    # user = get_object_or_404(User, username=request.POST.get('username'))
    # если поставить как сейчас выше, то выкидывает ошибку, что страница не найдена
    # если поставить внутри try, то try не проходит и выбрасывает 400 вместо 404
    # оба варианта не проходят тесты, поэтому действовал с try вместо get_object_or_404
    try:
        username = request.data['username']
        code = request.data['confirmation_code']
        try:
            user = User.objects.get(username=username)
        except Exception:
            return Response('Data not found', status=status.HTTP_404_NOT_FOUND)
        if username == user.username and code == user.confirmation_code:
            refresh_token = RefreshToken.for_user(user)
            data = {
                'token': str(refresh_token.access_token),
            }
        return Response(data)
    except Exception:
        return Response('Data is invalid', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def get_patch_user_data(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    else:
        user = User.objects.get(username=request.user)
        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            if user.role != ADMIN:
                serializer.save(role=user.role)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
