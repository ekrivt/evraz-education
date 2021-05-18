from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from datetime import  timedelta

from rest_framework.routers import DefaultRouter

from accounts import urls
from accounts.views import BaseView

from project import urls
from project.views import ProjectViewSet

from task import urls
from task.views import  DescriptionViewSet, TaskView 

from comment.views import CommentViewSet

router = DefaultRouter()
#router.register('project', ProjectViewSet)
#router.register('task', TaskView)
router.register('description', DescriptionViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('admin/', admin.site.urls, name = 'admin'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('api/accounts/',include('accounts.urls')),
    path('api/task/', include('task.urls')),
    path('api/project/', include('project.urls')),
]
