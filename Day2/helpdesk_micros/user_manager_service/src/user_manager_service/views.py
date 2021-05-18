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
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                username=username, password=password
            )
            if user:
                login(request, user)
                print('{} :Access granted'.format(user))
                return HttpResponseRedirect('/api/project')
        context = {
            'form': form,
        }
        return render(request, 'login.html', context, c)


class RegistrationView(View):

    def post( request, *args, **kwargs):
        print(request)
        new_user = User()
        
        body_unicode = request.body.decode('utf-8')
        print(request.body)
        body = json.dumps(body_unicode)
        print("body {}".format(body))

        new_user.username = body['username']
        new_user.password = body['password']
        new_user.save()
        '''new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        if form.cleaned_data['status'] == 'admin':
            new_user.is_staff = True
            new_user.is_superuser = True
            new_user.save()
        accounts.user = new_user
        accounts.status = form.cleaned_data['status']
        accounts.save()
            user = authenticate(
                username=new_user.username, 
                password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/api/project')
        context = {
            'form': form,
        }'''
        res = HttpResponse()
        res.status_code = 200
        return res