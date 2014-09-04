from django.contrib.auth.models import User
from django.db import models


class UserDictionary(models.Model):
    user = models.ForeignKey(User)
    word = models.CharField(max_length=255, unique=True)
    #
    # class Meta:
    #     ordering = ['word']