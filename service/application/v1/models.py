from django.db.models import (CheckConstraint, DateTimeField, F, ForeignKey,
                              Model, Q, TextField, CASCADE)
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(Model):
    author = ForeignKey(
        on_delete=CASCADE,
        related_name='tasks',
        to=User
    )
    description = TextField()
    finish_date = DateTimeField()
    start_date = DateTimeField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(finish_date__gt=F('start_date')),
                name='Finish date has to be greater than start date'
            )
        ]
        ordering = ('-start_date',)
