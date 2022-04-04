from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
