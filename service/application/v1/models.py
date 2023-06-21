from django.contrib.auth import get_user_model
from django.db.models import (CASCADE, CheckConstraint, DateTimeField, F,
                              ForeignKey, Model, Q, TextField)

User = get_user_model()


class Task(Model):
    author = ForeignKey(
        on_delete=CASCADE,
        related_name='tasks',
        to=User,
        verbose_name='Автор'
    )
    description = TextField(verbose_name='Описание')
    finish_date = DateTimeField(verbose_name='Начало')
    start_date = DateTimeField(verbose_name='Окончание')

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(finish_date__gt=F('start_date')),
                name='Finish date has to be greater than start date'
            )
        ]
        ordering = ('-start_date',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
