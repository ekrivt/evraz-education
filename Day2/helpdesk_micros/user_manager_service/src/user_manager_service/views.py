from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

'''class ProfileView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = () #(IsOwnerProfileOrReadOnly,IsAuthenticated,)

    def get_profile(self, serializer):
        serializer.save(author=self.request.user)'''