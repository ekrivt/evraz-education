from django.urls import include, path

from .views import (
    ProjectViewSet,
    ProjectViewList
)

urlpatterns = [
    path('project/', ProjectViewList.as_view(), name='projects'),
]