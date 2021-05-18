from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer
from .forms import LoginForm, RegistrationForm

User = get_user_model()
c = {}

class UserProfileListCreateView(ListCreateAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)
    

class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]

class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)

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
                return HttpResponseRedirect('/api/project')
        context = {
            'form': form,
        }
        return render(request, 'login.html', context, c)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        accounts = UserProfile()
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
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
        }
        return render(request, 'registration.html', context, c)

class BaseView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'base.html', context)
