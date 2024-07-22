from django.db import models
from django.conf import settings
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Адрес для рассылки')
    first_name = models.CharField(**NULLABLE, max_length=150, verbose_name='Имя')
    last_name = models.CharField(**NULLABLE, max_length=150, verbose_name='Фамилия')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневно'),
        (PERIOD_WEEKLY, 'Еженедельно'),
        (PERIOD_MONTHLY, 'Ежемесячно'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    )

    start_time = models.DateTimeField(verbose_name='Время запуска')
    end_time = models.DateTimeField(verbose_name='Время окончания', **NULLABLE)
    period = models.CharField(choices=PERIODS, default=PERIOD_DAILY, max_length=20, verbose_name='Период')
    status = models.CharField(choices=STATUSES, default=STATUS_CREATED, max_length=20, verbose_name='Статус')
    message = models.ForeignKey('MailingMessage', on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name='mailing_settings')

    def __str__(self):
        return f'{self.start_time} / {self.period}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылок'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'fail'
    STATUSES = (
        (STATUS_OK, 'успешно'),
        (STATUS_FAILED, 'ошибка'),
    )

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name='Получатель', null=True, blank=True)
    settings = models.ForeignKey(MailingSettings, on_delete=models.SET_NULL, verbose_name='Настройка', null=True,
                                 blank=True)
    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус')
    server_response = models.CharField(verbose_name='Статус', max_length=350, **NULLABLE)

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
