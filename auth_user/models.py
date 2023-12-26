from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class UserHasRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default="Aucun")

    def __str__(self):
        return self.user.username + "-" + self.role.name

