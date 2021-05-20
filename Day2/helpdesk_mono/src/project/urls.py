from django.urls import include, path

from .views import (
    ProjectViewSet,
    ProjectViewList
)

urlpatterns = [
    path('', ProjectViewList.as_view(), name='projects'),
]