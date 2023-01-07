from django.db import models

# Create your models here.

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    work = models.CharField(max_length=200, null=True)