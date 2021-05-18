from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from datetime import  timedelta

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
