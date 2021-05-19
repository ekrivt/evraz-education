from django.views.generic import DetailView, View
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .permission import IsOwnerProfileOrReadOnly
from .serializers import ProjectSerializer
from .models import Project
from .form import ProjectListForm

from task.models import Task

c = {}

class ProjectViewList(View):
    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerProfileOrReadOnly,IsAuthenticated)

    def get(self, request, *args, **kwargs):
        form = ProjectListForm(request.POST or None)
        projectlist = Project.objects.all()
        tasklist = Task.objects.all()
        context = {
            'form': form,
            'projects': projectlist,
            'tasks': tasklist,
            'auth': True
        }
        return render(request, 'projects.html', context)

    def post(self, request, *args, **kwargs):
        form = ProjectListForm(request.POST or None)
        projectlist = Project.objects.all()
        tasklist = Task.objects.all()
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.name = form.cleaned_data['name']
            new_project.save()

        context = {
            'form': form,
            'projects': projectlist,
            'tasks': tasklist,
            'auth': True
        }
        return render(request, 'projects.html', context, c)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = ()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super().get_permissions()