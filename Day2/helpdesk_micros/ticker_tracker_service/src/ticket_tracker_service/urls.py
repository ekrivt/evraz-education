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
#from task.views import TaskViewSet

router = DefaultRouter()
router.register('project', ProjectViewSet)
#router.register('task', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),

    #path('', include(router.urls)),
    path('', include(task.urls)),
    path('', include(project.urls)),
]
