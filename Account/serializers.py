from rest_framework import serializers
from djoser.serializers import UserCreateSerializer,UserSerializer
from .models import  *
from django.contrib.auth import authenticate
"""
les serializeurs CustomUserSerializer et UseLoginSerializer sont appelles dant viewTest.py
"""
class CustomUserSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ClientSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Client
        fields = '__all__'
# voici le serializeur dont j'utilise pour l'erigistrement d'un utilisateu 
class CustomUserSerializer2(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
# serializeur du login
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Unable to authenticate with provided credentials.')

        attrs['user'] = user
        return attrs
