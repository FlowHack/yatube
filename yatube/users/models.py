from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    avatar = models.ImageField(
        upload_to='profile_image',
        verbose_name='Аватарка',
        default='default_avatar.png'
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=200,
        default='У меня ещё нет статуса, но когда-то он должен появиться'
    )
