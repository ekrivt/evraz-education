from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from datetime import  timedelta

from rest_framework.routers import DefaultRouter

from .views import LoginView, RegistrationView

router = DefaultRouter()

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('login/', LoginView.post),
    path('registration/', RegistrationView.post)
]
