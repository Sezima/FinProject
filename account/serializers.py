from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import MyUser
from .utils import send_welcome_email


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password not right')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_welcome_email(email=user.email, activation_code=user.activation_code)
        return user

    def save(self, commit=True):
        user = MyUser.objects.create_user(**self.validated_data)
        send_welcome_email(user.email, user.activation_code)
        return user







class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                message = 'Unable to login'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include "email" and "password".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'avatar', 'id', 'followers', 'followings')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['followers'] = instance.followers.count()
        representation['followings'] = instance.followings.count()

        return representation


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username']





class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150, required=True)
    activation_code = serializers.CharField(max_length=100, min_length=6, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    def validate_activation_code(self, activation_code):
        if not MyUser.objects.filter(activation_code=activation_code, is_active=False).exists():
            raise serializers.ValidationError('Неверный код активации')
        return activation_code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.get(email=email, activation_code=code, is_active=False)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError('User not found')
        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user
