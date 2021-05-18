from django.db import models
from django.contrib.auth.models import User

from project.models import Project


class Task(models.Model):
    OPEN = 'open'
    RESOLVE = 'resolve'
    CANCEL = 'cancel'

    STATUS_CHOICES = (
        (OPEN, 'Открыт'),
        (RESOLVE, 'Решен'),
        (CANCEL, 'Отменен'),
    )

    name = models.CharField(max_length=50, verbose_name='Название задачи')
    project = models.ForeignKey(Project, verbose_name='Проект', related_name='task', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN, verbose_name='Статус')
    performer = models.ForeignKey(User, verbose_name='Исполнитель', related_name='task_performer', on_delete=models.SET_NULL,
                                  null=True, default=None)
    author = models.ForeignKey(User, verbose_name='Автор', related_name='task_author', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name

class Description(models.Model):
    task = models.ForeignKey(Task, verbose_name='Задача', related_name='description', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Описание')
    #author = models.ForeignKey(User, verbose_name='Автор', related_name='task_author', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
