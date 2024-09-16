import datetime

from django.db import models
from django.utils import timezone

from users.models import User


class Client(models.Model):
    name = models.CharField(max_length=20, verbose_name='имя', null=False, blank=False)
    surname = models.CharField(max_length=25, verbose_name='фамилия', null=False, blank=False)
    patronymic = models.CharField(max_length=25, verbose_name='отчество', null=False, blank=False)
    email = models.EmailField(verbose_name='почта', null=False, blank=False)
    comment = models.TextField(max_length=255, verbose_name="комментарий")
    company = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="компания", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f"{self.email}"


class Message(models.Model):
    header = models.CharField(max_length=100, verbose_name="заголовок сообщения")
    body = models.TextField(verbose_name="текст сообщения")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Sender(models.Model):
    FREQUENCIES = [
        ('ежедневно', 'Каждый день'),
        ('еженедельно', 'Раз в неделю'),
        ('ежемесячно', 'Раз в месяц'),
    ]

    STATUSES = [
        ("завершена", "Рассылка завершена"),
        ("создана", "Рассылка создана"),
        ("запущена", "Рассылка запущена")
    ]
    title = models.CharField(max_length=255, verbose_name='тема рассылки')
    company = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="компания", null=True, blank=True, default=None)
    clients = models.ManyToManyField(Client, verbose_name="клиенты", related_name='clients')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='сообщение', null=True, blank=True, default=None)
    created_at = models.DateTimeField(verbose_name="дата и время создания рассылки", auto_now_add=True)
    first_message = models.DateTimeField(verbose_name="дата и время первого письма", default=timezone.now())
    last_message = models.DateTimeField(verbose_name="дата и время последнего письма", default=timezone.now())
    date_letter_was_sent = models.DateTimeField(null=True, blank=True, verbose_name='дата когда нужно отправить следующее письмо')
    frequency = models.CharField(verbose_name="частота отправки", choices=FREQUENCIES)
    status = models.CharField(verbose_name="статус рассылки", choices=STATUSES)

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        permissions = [
            ("can_switch_sending", "can switch sending"),
        ]



class DeliveryAttempt(models.Model):
    attempt_datetime = models.DateTimeField(verbose_name='дата и время последней попытки')
    sender = models.ForeignKey(Sender,on_delete=models.CASCADE, verbose_name="рассылка для получения статуса и связи")
    mail_server_response = models.TextField(verbose_name='ответ почтового сервера', null=True, blank=True)

