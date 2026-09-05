from django.db import models

class User(models.Model):
    user_name=models.CharField(max_length=40,primary_key=True)
    password=models.CharField(max_length=140)
# Create your models here.
