from django.db import models
from django.contrib.auth.models import User

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