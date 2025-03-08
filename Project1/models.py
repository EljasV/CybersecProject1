from django.contrib.auth.models import User
from django.db import models


class Msg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()
