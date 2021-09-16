from django.db import models
from helpers.models import TrackingModel
from django.utils.translation import gettext_lazy as _
from authentication.models import User


class Todo(TrackingModel):
    title = models.CharField(max_length=125)
    body = models.TextField()
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('todo')
        verbose_name_plural = _('todos')