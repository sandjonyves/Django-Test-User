from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework import routers
from .viewTest import *
route = routers.SimpleRouter()
route.register('user',CustomUserViewSet2)
route.register('client',ClientViewSet)
route.register(r'read/user',readUser,basename='user')
urlpatterns = [
    path('',include(route.urls)),
    path('test',RegisterView.as_view(),name='register'),
    path('login',UserLoginView.as_view(),name='login')

]
