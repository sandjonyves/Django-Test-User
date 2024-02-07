from django.shortcuts import render
from djoser.views import UserViewSet
from django.http import JsonResponse
from rest_framework import permissions,viewsets
from .serializers import *
from .models import CustomUser
from rest_framework.decorators import action
# Create your views here.



class CustomUserViewSet(UserViewSet):
    # permissions =[permissions.AllowAny]
    serializer_class= CustomUserSerializer
    queryset =CustomUser.objects.all()
    

class CustomUserViewSet2(viewsets.ModelViewSet):
    # permissions =[permissions.AllowAny]
    serializer_class= CustomUserSerializer2
    queryset =CustomUser.objects.all()



class ClientViewSet(UserViewSet):
    # permissions =[permissions.AllowAny]
    serializer_class= ClientSerializer
    queryset =Client.objects.all()
    

class readUser(viewsets.ModelViewSet):
    serializer_class =CustomUserSerializer
   
    def get_queryset(self):
        queryset=CustomUser.objects.select_related('filiere')
        filiere_id = self.request.query_params.get('filiere_id')
        if filiere_id:
            queryset = queryset.filter(filiere__id=filiere_id)

        return queryset 
    @action(detail=False,methods=["get"],url_path="profile/(?P<id>\w+)")
    def profile(self,request,id):
        querysets = CustomUser.objects.filter(id=id)
        data =list(querysets.values('id','username','phone_number','email','filiere__name_filiere'))

        return JsonResponse(data,safe=False)