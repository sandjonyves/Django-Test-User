from django.shortcuts import render
from djoser.views import UserViewSet
from django.http import JsonResponse
from rest_framework import permissions,viewsets
from .serializers import *
from .models import CustomUser
from rest_framework.decorators import action
from rest_framework import generics ,status
import secrets
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from django.core.management import call_command
from django.utils.timezone import now
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import  UserLoginSerializer

class RegisterView(generics.CreateAPIView):

    authentication_classes=[
        BasicAuthentication
    ]
    serializer_class =CustomUserSerializer2
    permission_classes =[AllowAny]

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                 {"error": "Please provide the required fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email =serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
 
        try:
            if (
                    email
                    and CustomUser.objects.exclude(email__isnull=True)
                    .exclude(email__exact="")
                    .filter(email=email.lower())
                    .exists()
            ):
                return Response(
                    {"error": "User with this email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

          
            if (
                    username
                    and CustomUser.objects.exclude(username__isnull=True)
                    .exclude(username__exact="")
                    .filter(username=username)
                    .exists()
            ):
                return Response(
                    {"error": "User with this username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except IntegrityError:
            return Response(
                {"error": "Integrity error"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        user.save()
        return Response(
            {"success": "User registered successfully. Go ahead and login."},
            status=status.HTTP_201_CREATED,
        )



class LoginView(APIView):
    
    def post(self, request):
        email = request.data['data']
        username = request.data['username'
                                ]
        print("111111111111111111111111111111111111111111111111")
        user = CustomUser.objects.filter(username=username).first()
       
        if not user:
            raise AuthenticationFailed('user not found')
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)       
        return Response({'message':'success'})

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    #     authentication_classes = [
    #     OAuth2Authentication,
        
    # ]
    permission_classes=[AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data['username'
                                    ]
        password = request.data['password']
        print("111111111111111111111111111111111111111111111111")
        user = CustomUser.objects.filter(username=username).first()
        if user.check_password(password):
            if not user.is_active:
                raise ValueError("User account is not active")
            # if not user.phone_number_verified and email_or_phone.startswith("+"):
            #     raise ValueError("Phone number not verified")

        if not user:
            raise AuthenticationFailed('user not found')       
        serializer = self.get_serializer(data=request.data)
        print("2222222222222222222222222222222222222222")
        # serializer.is_valid(raise_exception=True)
        print("33333333333333333333333333333333333333")
        serializer.is_valid(raise_exception=True)
        errors = serializer.errors

        for field, error_msgs in errors.items():
            print(f"Field: {field}")
            for msg in error_msgs:
                print(f"Error: {msg}")
        refresh = RefreshToken.for_user(user)
        print("4444444444444444444444444444444444444444444444444")
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)