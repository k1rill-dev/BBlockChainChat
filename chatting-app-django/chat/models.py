from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='sender', verbose_name='Отправитель')
    receiver = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE, related_name='receiver', verbose_name='Получатель')
    message = models.CharField(max_length=1200, verbose_name='Сообщение')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время отправления')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    hash_bloks = models.CharField(max_length=200, default=0)
    full_name_send = models.CharField(max_length=255, verbose_name='Полное имя отправителя', blank=True, null=True)
    full_name_receiver = models.CharField(max_length=255, verbose_name='Полное имя получателя', blank=True, null=True)

    def __str__(self):
        return f"{self.message}"

    class Meta:
        ordering = ('timestamp',)
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'

class Profile(models.Model):
    user = models.IntegerField(blank=True)
    open_key = models.CharField(max_length=100, blank=True)
    secret_key = models.CharField(max_length=100, blank=True)
    aes_key = models.CharField(max_length=100, blank=True)