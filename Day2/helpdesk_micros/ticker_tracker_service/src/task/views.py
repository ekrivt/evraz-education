from django.db.models import Q
from django.views.generic import DetailView, View
import requests
import json
from django.shortcuts import render
from requests.api import request
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListCreateAPIView

from .models import Task, Description, UserProfile
from .form import TaskListForm
from .permission import IsOwnerProfileOrReadOnly
from .serializers import TaskSerializer, DescriptionSerializer, ProfileSerializer

c = {}

def get_token():
    post_data = {
        'username': 'admin',
        'password': '1q2w3e4r5!'
        }
    response = requests.post('http://user-service:8000/auth/jwt/create/', data=post_data)
    token = response.json().get('access')
    return token

def get_userlist():
        res=requests.get('http://user-service:8000/auth/users/', headers={'Authorization': 'Bearer {}'.format(get_token())})
        return res.json().get('results')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = () #(IsOwnerProfileOrReadOnly,IsAuthenticated,)

    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('performer__username', 'author__username',
                     'name', 'project__name', 'status', 'description__text')
    ordering_fields = '__all__'
    ordering = ('-id',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(Q(author=user.pk) | Q(performer=user.pk))
        return queryset

class ProfileView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = () #(IsOwnerProfileOrReadOnly,IsAuthenticated,)

    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('performer__username', 'author__username',
                     'name', 'project__name', 'status', 'description__text')
    ordering_fields = '__all__'
    ordering = ('-id',)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(Q(author=user.pk) | Q(performer=user.pk))
        return queryset

class TaskDetailView(View):
    serializer_class = TaskSerializer
    permission_classes = ()
    user = get_userlist()[0]
    name = user.get('username')

    def get(self, request, *args, **kwargs):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        context = {
            'form': form,
            'tasks': tasks,
            'account': self.name
        }
        return render(request, 'task.html', context)

    def get_task_by_id(request, task_id):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        context = {
            'form': form,
            'tasks': tasks.filter(pk=task_id),
            #'account': name
        }
        return render(request, 'task.html', context)

class TaskView(View):
    serializer_class = TaskSerializer
    permission_classes = ()
    user = get_userlist()[0]
    name = user.get('username')

    def get(self, request, *args, **kwargs):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        context = {
            'form': form,
            'tasks': tasks,
            'account': self.name
        }
        return render(request, 'task.html', context)

    def post(self, request, *args, **kwargs):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.name = form.cleaned_data['name']
            new_task.save()
            new_task.project = form.cleaned_data['project']
            new_task.save()
            new_task.status = form.cleaned_data['status']
            new_task.save()
            new_task.performer = self.name
            new_task.save()
            new_task.author = self.name
            new_task.save()

        context = {
            'form': form,
            'tasks': tasks,
        }
        return render(request, 'task.html', context, c)

class UserProfileDetailView(viewsets.ModelViewSet):
    queryset=UserProfile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[]

    def post_queryset(self):
        post_data = {
            'username': 'admin',
            'password': '1q2w3e4r5!'
            }
        response = requests.post('http://user-service:8000/auth/jwt/create/', data=post_data, auth=('admin', '1q2w3e4r5!'))
        token = response.json().get('access')
        return response#{ 'token':token }

    