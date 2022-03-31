from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import CustomUserSerializer
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = random.randint(10000, 20000)
        serializer.save(code=confirmation_code)
        email = serializer.data['email']
        message = 'Your confirmation code: ' + str(confirmation_code)
        send_mail(
            'Confirmation code',
            message,
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain(request):
    try:
        username = request.data['username']
        code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if username == user.username and code == str(user.code):
            access_token = RefreshToken.for_user(user).access_token
            data = {
                'token': str(access_token),
            }
        return Response(data)
    except:
        return Response('Data is invalid', status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PATCH'])
# def patch_user_data(request):
#     serializer = CustomUserSerializer(data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
