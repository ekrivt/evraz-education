from django.urls import include, path

from .views import (
    #TaskViewSet,
    TaskView,
    TaskDetailView,
    DescriptionViewSet
)

urlpatterns = [
    path('', TaskView.as_view(), name='task'),
    path('<int:task_id>/', TaskDetailView.get_task_by_id),
]