from django.db import models

# Create your models here.
class user_db(models.Model):
    user_nm = models.CharField(max_length=30)
    email = models.CharField(max_length=30) 
    password = models.CharField(max_length=30)
class admin_db(models.Model):
    admin_nm = models.CharField(max_length=30)
    email = models.CharField(max_length=30) 
    password = models.CharField(max_length=30)
    