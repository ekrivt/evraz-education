from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название проекта')

    def __str__(self):
        return self.name
