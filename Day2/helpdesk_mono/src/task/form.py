from django import forms
from django.db import models
from django.contrib.auth import get_user_model

from .models import Task

from project.views import Project

User = get_user_model()

OPEN = 'open'
RESOLVE = 'resolve'
CANCEL = 'cancel'

STATUS_CHOICES = (
    (OPEN, 'Открыт'),
    (RESOLVE, 'Решен'),
    (CANCEL, 'Отменен')
)

class TaskListForm(forms.ModelForm):

    project_list = Project.objects.all()
    users_list = User.objects.all()
    
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['name', 'project', 'status', 'performer', 'author','description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['project'].label = 'Проект'
        self.fields['status'].label = 'Статус'
        self.fields['performer'].label = 'Исполнитель'
        self.fields['description'].lable = 'Описание'

    def clean_name(self):
        name = self.cleaned_data['name']
        if Task.objects.filter(name=name).exists():
            raise forms.ValidationError(
                'Название занято'
            )
        return name
    
    