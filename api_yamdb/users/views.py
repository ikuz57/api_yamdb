import random

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import CustomUserSerializer, CustomUserSerializerShort
from .models import ADMIN
from .utils import send_email_with_code

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
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
@permission_classes([permissions.AllowAny])
def token_obtain(request):
    username = request.data.get('username')
    code = request.data.get('confirmation_code')
    if username is None or code is None:
        return Response('Data is invalid',
                        status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    if username == user.username and code == user.confirmation_code:
        refresh_token = RefreshToken.for_user(user)
        data = {
            'token': str(refresh_token.access_token),
        }
        return Response(data)
    return Response('Data is invalid',
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'

    def get_permissions(self):

        if self.action in [
            'list',
            'create',
            'retrieve',
            'update',
            'partial_update',
            'destroy'
        ]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve_me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update_me(self, request, pk=None):
        user = request.user
        serializer = self.get_serializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            if user.role != ADMIN:
                serializer.save(role=user.role)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
