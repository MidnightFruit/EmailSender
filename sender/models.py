from django.db import models

from users.models import Company


class Client(models.Model):
    name = models.CharField(max_length=20, verbose_name='имя', null=False, blank=False)
    surname = models.CharField(max_length=25, verbose_name='фамилия', null=False, blank=False)
    patronymic = models.CharField(max_length=25, verbose_name='отчество', null=False, blank=False)
    email = models.EmailField(unique=True, verbose_name='почта', null=False, blank=False)
    comment = models.TextField(max_length=255, verbose_name="комментарий")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="компания", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f"{self.name} {self.patronymic} {self.email}"


class Message(models.Model):
    header = models.CharField(max_length=100, verbose_name="заголовок сообщения")
    body = models.TextField(verbose_name="текст сообщения")
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, default=None)

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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="компания", null=True, blank=True, default=None)
    clients = models.ManyToManyField(Client, verbose_name="клиенты", related_name='clients')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='сообщение', null=True, blank=True, default=None)
    created_at = models.DateTimeField(verbose_name="дата и время первого сообщения", auto_now_add=True)
    frequency = models.CharField(verbose_name="частота отправки", choices=FREQUENCIES)
    status = models.CharField(verbose_name="статус рассылки", choices=STATUSES)

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"



class DeliveryAttempt(models.Model):
    attempt_datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    attempt_status = models.BooleanField(default=False, verbose_name="статус попытки")
    mail_server_response = models.TextField(verbose_name='ответ почтового сервера', null=True, blank=True)

