from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth.models import User

import requests
from requests import status_codes
import json

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

c = {}

'''class ProfileView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = () #(IsOwnerProfileOrReadOnly,IsAuthenticated,)

    def get_profile(self, serializer):
        serializer.save(author=self.request.user)'''

class LoginView(View):

    def post(request, *args, **kwargs):

        body_unicode = request.body.decode('utf-8')
        print(request.body)
        body = json.loads(body_unicode)
        print("body {}".format(body))

        username = body['username']
        password = body['password']

        if not User.objects.filter(username=username).exists():
            return HttpResponseNotFound()
        user = User.objects.filter(username=username).first()
        if user:
            if user.password != password:
                return HttpResponseBadRequest()

        '''user = authenticate(
            username=username, password=password
            )'''
        
        return HttpResponse("Login OK")


class RegistrationView(View):

    def post(request, *args, **kwargs):
        new_user = User()
        body_unicode = request.body.decode('utf-8')
        print(request.body)
        body = json.loads(body_unicode)
        print("body {}".format(body))

        username = body['username']
        password = body['password']

        if User.objects.filter(username=username).exists():
            return HttpResponse(status=status.HTTP_409_CONFLICT)

        new_user.username = username
        new_user.password = password
        new_user.save()

        return HttpResponse("Registration OK")