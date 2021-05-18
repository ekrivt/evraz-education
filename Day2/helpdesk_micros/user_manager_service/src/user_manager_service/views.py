from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
import requests
from requests import status_codes
import json

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

c = {}

'''class ProfileView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = () #(IsOwnerProfileOrReadOnly,IsAuthenticated,)

    def get_profile(self, serializer):
        serializer.save(author=self.request.user)'''

class LoginView(View):

    def post(self, request, *args, **kwargs):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(
            username=username, password=password
        )
        if user:
            print('{} :Access granted'.format(user))

        res = HttpResponse()
        res.status_code = 200
        return res


class RegistrationView(View):

    def post( request, *args, **kwargs):
        new_user = User()
        body_unicode = request.body.decode('utf-8')
        print(request.body)
        body = json.loads(body_unicode)
        print("body {}".format(body))

        new_user.username = body['username']
        new_user.password = body['password']
        new_user.save()

        res = HttpResponse()
        res.status_code = 200
        return res