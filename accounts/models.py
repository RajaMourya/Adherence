from django.db import models

# Create your models here.
class Patient(models.Model):
    first = models.CharField(max_length=30)
    last = models.CharField(max_length=30)
    email = models.EmailField()
    contact = models.CharField(max_length=10)
    payer = models.CharField(max_length=10)
    medical = models.IntegerField()
    treatment = models.IntegerField()
    total = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    blood = models.CharField(max_length=10)
    emergency = models.EmailField(max_length=10)
    address = models.CharField(max_length=20)
    town = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=10)
