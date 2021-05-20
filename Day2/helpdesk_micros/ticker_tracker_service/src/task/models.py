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
    performer = models.CharField(max_length=50, verbose_name='Исполнитель', null=True, default=None)
    author = models.CharField(max_length=50, verbose_name='Автор')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name

class Description(models.Model):
    task = models.ForeignKey(Task, verbose_name='Задача', related_name='description', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.text

class UserProfile(models.Model):

    ADMIN = 'admin'
    STAFF = 'staff'
    CLIENT = 'client'

    STATUS_CHOICES = (
        (ADMIN, 'Администратор'),
        (STAFF, 'Персонал'),
        (CLIENT, 'Клиент')
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="Профиль")
    description=models.TextField(blank=True,null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CLIENT, verbose_name='Статус')
    date_joined=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    is_organizer=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
