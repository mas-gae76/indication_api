from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.dispatch import receiver
from django.db.models.signals import post_save


class Counter(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(verbose_name='Название', max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Клиент')
    value = models.PositiveIntegerField(verbose_name='Текущие показания', default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Счётчик'
        verbose_name_plural = 'Счётчики'


class History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateField(verbose_name='Дата', auto_now_add=True)
    type = models.BooleanField(verbose_name='Оператор?', default=False)
    value = models.PositiveIntegerField(verbose_name='Показания')
    consumption = models.PositiveIntegerField(verbose_name='Расход')
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE, verbose_name='Счётчик')

    def __str__(self):
        return f'{self.date}: {self.value}'

    class Meta:
        verbose_name = 'Показание'
        verbose_name_plural = 'Показания'
        ordering = ('-date', )


@receiver(post_save, sender=Counter)
def signal_handler(sender, instance, **kwargs):
    existed = History.objects.filter(counter=instance).exists()
    if existed:
        prev_value = History.objects.filter(counter=instance).order_by('-value').first().value
        History.objects.create(value=instance.value, consumption=instance.value - prev_value, counter=instance)
    else:
        History.objects.create(value=instance.value, consumption=instance.value, counter=instance)
