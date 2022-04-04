from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializerShort(serializers.ModelSerializer):

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Поле не может быть "me".'
            )
        return username

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
