import os
import random

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db import transaction
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    def avatar_upload(self, filename):
        return os.path.join('users', str(self.pk), 'avatars', filename)

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=True, default="")
    name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    rows_to_recalculate_available = models.IntegerField(default=1000)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.name if self.name else "USER_" + str(self.pk)


class UserUniqueToken(models.Model):
    ACTIONS = (
        ('register', 'Регистрация',),
        ('pass_reset', 'Сброс пароля',),
    )
    action = models.CharField(max_length=10, choices=ACTIONS, default='register')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    token = models.TextField(editable=False, unique=True)
    expire = models.DateTimeField(editable=False)

    @staticmethod
    def generate(user: User, act: str):
        s = 'QWERYIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
        ln = 150
        t = ''.join([random.choice(s) for _ in range(ln)])
        while UserUniqueToken.objects.filter(token=t).exists():
            t = ''.join([random.choice(s) for _ in range(ln)])
        return UserUniqueToken.objects.create(
            token=t, user=user, expire=timezone.localtime(timezone.now()) + timezone.timedelta(days=7), action=act)
