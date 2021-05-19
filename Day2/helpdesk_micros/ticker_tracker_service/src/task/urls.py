from django.urls import include, path
from requests.models import Response

from .views import (
    LoginView,
    RegistrationView,
    TaskViewSet,
    UserProfileDetailView,
    TaskView,
    TaskDetailView,
    LoginView,
    RegistrationView,
    LogoutView
)

urlpatterns = [
    path('task/<int:task_id>/', TaskDetailView.get_task_by_id),
    path('task/<int:task_id>/open', TaskDetailView.change_status_open),
    path('task/<int:task_id>/resolve', TaskDetailView.change_status_resolve),
    path('task/<int:task_id>/cancel', TaskDetailView.change_status_cancel),

    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.logout, name='logout'),

    path('jwt/', UserProfileDetailView.post_queryset),
    path('task/', TaskView.as_view(), name='base'),
]