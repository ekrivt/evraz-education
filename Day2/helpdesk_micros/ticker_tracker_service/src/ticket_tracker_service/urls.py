from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from datetime import  timedelta

from rest_framework.routers import DefaultRouter

import project
from project import urls
from project.views import ProjectViewSet

import task
from task import urls

router = DefaultRouter()
router.register('project', ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),

    
    path('', include(task.urls)),
    path('', include(project.urls)),
]
