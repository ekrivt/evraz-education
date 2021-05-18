from django.urls import include, path

from .views import (
    TaskViewSet,
    UserProfileDetailView,
    TaskView,
    TaskDetailView
)

urlpatterns = [
    #path('', TaskViewSet.as_view(), name='task'),
    path('task/<int:task_id>/', TaskDetailView.get_task_by_id),

    path('jwt/', UserProfileDetailView.post_queryset),
    path('task/', TaskView.as_view(), name='base'),
]