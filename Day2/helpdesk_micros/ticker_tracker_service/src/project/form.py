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

    #name = forms.CharField(max_length=100)
    '''#project = forms.ChoiceField(choices = project_list)
    status = forms.ChoiceField(choices = STATUS_CHOICES)
    #performer = forms.ChoiceField(choices = users_list)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['name', 'project', 'status', 'performer', 'author' ,'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'
        self.fields['project'].label = 'Проект'
        self.fields['status'].label = 'Статус'
        self.fields['performer'].label = 'Исполнитель'
        self.fields['description'].lable = 'Описание' '''

    