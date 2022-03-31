from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import CustomUserSerializer, MyTokenObtainPairSerializer
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def signUp(request):
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
