import datetime
from django.contrib.auth.models import User
from django.db import models


class UserDictionary(models.Model):
    user = models.ForeignKey(User)
    word = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'word')