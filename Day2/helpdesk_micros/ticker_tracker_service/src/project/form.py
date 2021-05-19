from django import forms
from django.db import models
from django.contrib.auth import get_user_model

from .models import Project

User = get_user_model()

class ProjectListForm(forms.ModelForm):

    project_list = Project.objects.all()
    users_list = User.objects.all()

    class Meta:
        model = Project
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'

    def clean_name(self):
        name = self.cleaned_data['name']
        if Project.objects.filter(name=name).exists():
            raise forms.ValidationError(
                'Название занято'
            )
        return name

    