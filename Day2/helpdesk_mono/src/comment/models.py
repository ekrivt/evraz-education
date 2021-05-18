from django.db import models
from django.contrib.auth.models import User

from task.models import Task


class Comment(models.Model):
    task = models.ForeignKey(Task, verbose_name='Задача', related_name='comment', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Коммент')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
