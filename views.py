from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from . serializers import Userserializer
from rest_framework.exceptions import AuthenticationFailed
from users.models import User,Article as ART
import json
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from django.core import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from .authentication import token_expire_handler, expires_in
from django.contrib.auth import logout

def wrapper(request):
    username=request.data['username']
    password=request.data['password']

    user =authenticate(
            username= username,
            password = password
        )
    return user


class Register(APIView):
    def post(self, request):
        print(type(request))
        serializer=Userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(type(serializer.data))
        return Response(serializer.data)
    
class Login(APIView):
    def post(self, request):
        user=wrapper(request)
        if not user:
            return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user = user)
        is_expired, token = token_expire_handler(token)     
        return Response({
         'user':user.username,
         'expires_in': expires_in(token),
       'token': token.key
    }, status=HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class Userview(APIView):
    
    def get(self,request):
        obj=ART.objects.all().values()
        return Response(obj, content_type='application/json')
    
    def post(self,request):
        obj=Token.objects.filter(key=request.auth.key).all().values()
        print(obj)
        for i in obj:
            id=i["user_id"]
        object=User.objects.filter(id=id).all().values()
        return Response(object, content_type='application/json')
    
class Logoutview(APIView):

    def post(self, request):
        user=wrapper(request)
        if not user:
            return Response({'detail': 'Invalid Credentials '}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user = user)
        try:
            request.user.auth_token.delete()
        except (AttributeError, ValueError):
                pass
        logout(request)  
        return Response(
             {
                'message':'User has been logout' ,
                "deleted token": token.key

             }, status=HTTP_200_OK)
         

class Refereshtoken(APIView):
    def post(self,request):
        user=wrapper(request)
        if not user:
            return Response({'detail': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user = user)
        if token:
            token.delete()
        token, _ = Token.objects.get_or_create(user = user)
        return Response(
             {
                'message':'New token has been generated' ,
                "New token": token.key
             }, status=HTTP_200_OK)
        
         
        