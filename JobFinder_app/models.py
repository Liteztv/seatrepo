from django.db import models
from django.contrib.auth.models import User




# class NameModel(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)

class SeekerModel(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    total_years_experience = models.IntegerField()
    
    


