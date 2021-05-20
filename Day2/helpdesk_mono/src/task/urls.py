from django.urls import include, path

from .views import (
    TaskView,
    TaskDetailView,
    DescriptionViewSet
)

urlpatterns = [
    path('', TaskView.as_view(), name='task'),
    path('<int:task_id>/', TaskDetailView.get_task_by_id),
    path('<int:task_id>/open', TaskDetailView.change_status_open),
    path('<int:task_id>/resolve', TaskDetailView.change_status_resolve),
    path('<int:task_id>/cancel', TaskDetailView.change_status_cancel),
    
]