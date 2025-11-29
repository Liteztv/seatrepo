from django.db import models
from django.contrib.auth.models import User




# class NameModel(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)

class SeekerModelOne(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    total_years_of_experience = models.IntegerField(null=True)
    html_experience = models.IntegerField(null=True)
    css_experience = models.IntegerField(null=True,verbose_name='CSS Experience')

class SeekerModelTwo(models.Model):    
    python_experience = models.IntegerField(null=True)
    java_experience = models.IntegerField(null=True)
    javascript_experience = models.IntegerField(null=True, verbose_name='JavaScript Experience')
    cplusplus_experience = models.IntegerField(null=True, verbose_name='C++ Experience')
    csharp_experience = models.IntegerField(null=True, verbose_name='C# Experience')
    ruby_experience = models.IntegerField(null=True)

class SeekerModelThree(models.Model):
    react_experience = models.IntegerField(null=True)
    vue_experience = models.IntegerField(null=True, verbose_name='Vue.js Experience')
    angular_experience = models.IntegerField(null=True)
    django_experience = models.IntegerField(null=True)
    flask_experience = models.IntegerField(null=True)
    ruby_on_rails_experience = models.IntegerField(null=True)
    fastapi_experience = models.IntegerField(null=True, verbose_name='FastAPI Experience')
    laravel_experience = models.IntegerField(null=True)
    express_experience = models.IntegerField(null=True, verbose_name='Express.js Experience')
    springboot_experience = models.IntegerField(null=True)
    aspnet_experience = models.IntegerField(null=True, verbose_name='ASP.NET Experience')
    oracle_experience = models.IntegerField(null=True)
    mysql_experience = models.IntegerField(null=True, verbose_name='mySQL Experience')
    sqlite_experience = models.IntegerField(null=True, verbose_name='SQLite Experience')
    mongodb_experience = models.IntegerField(null=True)
    postgresql_experience = models.IntegerField(null=True, verbose_name='PostgreSQL Experience')

class EmployerModelOne(models.Model):
    total_years_of_experience = models.IntegerField(null=True)
    html_experience = models.IntegerField(null=True)
    css_experience = models.IntegerField(null=True, verbose_name='CSS Experience')
    
class EmployerModelTwo(models.Model):
    python_experience = models.IntegerField(null=True)
    java_experience = models.IntegerField(null=True)
    javascript_experience = models.IntegerField(null=True, verbose_name='JavaScript Experience')
    cplusplus_experience = models.IntegerField(null=True, verbose_name='C++ Experience')
    csharp_experience = models.IntegerField(null=True, verbose_name='C# Experience')
    ruby_experience = models.IntegerField(null=True)

class EmployerModelThree(models.Model):
    react_experience = models.IntegerField(null=True)
    vue_experience = models.IntegerField(null=True, verbose_name='Vue.js Experience')
    angular_experience = models.IntegerField(null=True)
    django_experience = models.IntegerField(null=True)
    flask_experience = models.IntegerField(null=True)
    ruby_on_rails_experience = models.IntegerField(null=True)
    fastapi_experience = models.IntegerField(null=True, verbose_name='FastAPI Experience')
    laravel_experience = models.IntegerField(null=True)
    express_experience = models.IntegerField(null=True, verbose_name='Express.js Experience')
    springboot_experience = models.IntegerField(null=True)
    aspnet_experience = models.IntegerField(null=True, verbose_name='ASP.NET Experience')
    oracle_experience = models.IntegerField(null=True)
    mysql_experience = models.IntegerField(null=True, verbose_name='mySQL Experience')
    sqlite_experience = models.IntegerField(null=True, verbose_name='SQLite Experience')
    mongodb_experience = models.IntegerField(null=True)
    postgresql_experience = models.IntegerField(null=True, verbose_name='PostgreSQL Experience')



    
    


