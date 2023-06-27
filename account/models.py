from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    phone_number = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=220, blank=True)
    location = models.PointField()
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_group')
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permission")
