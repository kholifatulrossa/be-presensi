from django.db import models
from ..api.models import Guru
from ..api.models import Siswa

from django.contrib.auth.models import AbstractUser
from rest_framework import serializers, permissions, views
from rest_framework.response import Response


# Create your models here.
class User(AbstractUser):
    password = models.CharField(max_length=200)
    token = models.CharField(max_length=200, blank=True, null=True)
    guruId = models.ForeignKey(Guru, null=True, blank=True, on_delete=models.CASCADE)
    siswaId = models.ForeignKey(Siswa, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user'
        
    def __str__(self):
        return self.nama
    