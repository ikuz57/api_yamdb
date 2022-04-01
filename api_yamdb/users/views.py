from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import CustomUserSerializer
from .utils import send_email_with_code
import random
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    confirmation_code = str(random.randint(10000, 20000))
    try:
        user = User.objects.get(username=request.data['username'])
        user.confirmation_code = confirmation_code
        user.save()
        send_email_with_code(user.email, confirmation_code)
        return Response('Please verify your email', status=status.HTTP_201_CREATED)
    except:
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(confirmation_code=confirmation_code)
            send_email_with_code(serializer.data['email'], confirmation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain(request):
    try:
        username = request.data['username']
        code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if username == user.username and code == user.confirmation_code:
            access_token = RefreshToken.for_user(user).access_token

            data = {
                'token': str(access_token),
            }
        return Response(data)
    except:
        return Response('Data is invalid', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@staff_member_required
def patch_get_user_data(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    else:
        user = User.objects.get(username=request.user)
        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAdminUser,)
