from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import os


class PostTopic(models.Model):
    name = models.CharField(max_length=250, unique=True)


class Post(models.Model):
    def img_upload(self, filename):
        return os.path.join('faq', str(self.id), filename)

    topic = models.ForeignKey('application_info.PostTopic', on_delete=models.SET_NULL, null=True, default=None)
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to=img_upload, blank=True, null=True, default=None)
    short_text = models.TextField(blank=True, verbose_name='Короткий текст')
    article = models.TextField(blank=True)
    publication_time = models.DateTimeField(default=None, null=True, blank=True)
    saw_users = models.ManyToManyField('accounts.User', blank=True)
    is_faq = models.BooleanField(default=False)
    is_notify = models.BooleanField(default=False)
    is_news = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        unique_together = ('topic', 'name',)


class PostImg(models.Model):
    def img_upload(self, filename):
        return os.path.join('post', str(self.post_id), 'images', filename)

    post = models.ForeignKey('application_info.Post', on_delete=models.CASCADE)
    img = models.ImageField(upload_to=img_upload)


class Review(models.Model):
    grade = models.PositiveIntegerField(default=5, validators=[
        MaxValueValidator(5, message='Оценка не может быть больше 5'),
        MinValueValidator(1, message='Оценка не может быть меньше 1')
    ], editable=False)
    text = models.TextField(blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)


class ReviewImg(models.Model):
    def img_upload(self, filename):
        return os.path.join('reviews', str(self.id), filename)

    review = models.ForeignKey('application_info.Review', on_delete=models.CASCADE)
    img = models.ImageField(upload_to=img_upload)

    def __str__(self):
        return f'{self.id}, {self.review.__str__()}'

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class SystemConfig(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=10)
    version_suffix = models.CharField(max_length=10)
    is_actual = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not SystemConfig.objects.filter(is_actual=True).exists():
            self.is_actual = True
        elif self.is_actual:
            SystemConfig.objects.update(is_actual=False)
        return super().save(*args, **kwargs)


class Log(models.Model):
    SECTIONS = (
        ('system', 'Система',),
        ('recalculates', 'Пересчеты',),
        ('accounts', 'Аккаунты',),
        ('application_info', 'Информация о приложении',),
        ('statistic', 'Статистика',),
    )

    section = models.CharField(max_length=30, choices=SECTIONS, default='system')
    action = models.CharField(max_length=100)
    is_error = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    static_user_id = models.CharField(max_length=36, blank=True)
    user_email = models.CharField(max_length=250, blank=True)
    user_name = models.CharField(max_length=250, blank=True)
    log = models.TextField()
    system_version = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
