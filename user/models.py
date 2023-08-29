from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.

class UserOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    timme_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()

