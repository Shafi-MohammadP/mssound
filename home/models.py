from django.db import models

# Create your models here.


class Contacts(models.Model):

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, blank=True)
    email = models.EmailField()
    subject = models.EmailField()
    message = models.TextField()
