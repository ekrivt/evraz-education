from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

from .views import (
    LoginView,
    RegistrationView,
    UserProfileListCreateView, 
    UserProfileDetailView,

)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),

    path("all-profiles",UserProfileListCreateView.as_view(),name="all-profiles"),
    path("profile/<int:pk>",UserProfileDetailView.as_view(),name="profile"),
]