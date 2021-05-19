from django.db.models import Q
from django.views.generic import DetailView, View
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListCreateAPIView

from accounts.models import UserProfile

from .models import Task, Description
from .form import TaskListForm
from .permission import IsOwnerProfileOrReadOnly
from .serializers import TaskSerializer, DescriptionSerializer

c = {}

Users = get_user_model()

class TaskView(View):
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerProfileOrReadOnly,IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        user = UserProfile.objects.get(user=self.request.user)
        context = {
            'form': form,
            'tasks': tasks,
            'account': user
        }
        return render(request, 'task.html', context)

    def post(self, request, *args, **kwargs):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        user = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.name = form.cleaned_data['name']
            new_task.save()
            new_task.project = form.cleaned_data['project']
            new_task.save()
            new_task.status = form.cleaned_data['status']
            new_task.save()
            new_task.performer = form.cleaned_data['performer']
            new_task.save()
            new_task.author = self.request.user
            new_task.save()

        context = {
            'form': form,
            'tasks': tasks,
            'account': user
        }
        return render(request, 'task.html', context, c)

class TaskDetailView(View):
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerProfileOrReadOnly,IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        user = UserProfile.objects.get(user=self.request.user)
        context = {
            'form': form,
            'tasks': tasks,
            'account': user,
            'id': False
        }
        return render(request, 'task.html', context)

    def get_task_by_id(request, task_id):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()
        user = UserProfile.objects.get(user=request.user)
        context = {
            'form': form,
            'tasks': tasks.filter(pk=task_id),
            'account': user,
            'id' : True 
        }
        return render(request, 'task.html', context)

    def change_status_open(request, task_id):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()

        task = Task.objects.get(pk=task_id)
        task.status = 'open'
        task.save()

        user = UserProfile.objects.get(user=request.user)
        context = {
            'form': form,
            'tasks': tasks.filter(pk=task_id),
            'account': user
        }
        return HttpResponseRedirect('/api/task/{}'.format(task_id))

    def change_status_resolve(request, task_id):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()

        task = Task.objects.get(pk=task_id)
        task.status = 'resolve'
        task.save()

        user = UserProfile.objects.get(user=request.user)
        context = {
            'form': form,
            'tasks': tasks.filter(pk=task_id),
            'account': user
        }
        return HttpResponseRedirect('/api/task/{}'.format(task_id))

    def change_status_cancel(request, task_id):
        form = TaskListForm(request.POST or None)
        tasks = Task.objects.all()

        task = Task.objects.get(pk=task_id)
        task.status = 'cancel'
        task.save()

        user = UserProfile.objects.get(user=request.user)
        context = {
            'form': form,
            'tasks': tasks.filter(pk=task_id),
            'account': user
        }
        return HttpResponseRedirect('/api/task/{}'.format(task_id))

class DescriptionViewSet(viewsets.ModelViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    permission_classes = (IsOwnerProfileOrReadOnly,IsAuthenticated)
