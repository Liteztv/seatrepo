from django.db import models
from django.contrib.auth.models import User





class Profile(models.Model):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )

    user = models.OneToOneField(
        User,null=True,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} - {self.role or 'No role set'}"

class SeekerModelOne(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    total_years_of_experience = models.IntegerField(null=True)
    html_experience = models.IntegerField(null=True)
    css_experience = models.IntegerField(null=True,verbose_name='CSS Experience')

class SeekerModelTwo(models.Model):   
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE) 
    python_experience = models.IntegerField(null=True)
    java_experience = models.IntegerField(null=True)
    javascript_experience = models.IntegerField(null=True, verbose_name='JavaScript Experience')
    cplusplus_experience = models.IntegerField(null=True, verbose_name='C++ Experience')
    csharp_experience = models.IntegerField(null=True, verbose_name='C# Experience')
    ruby_experience = models.IntegerField(null=True)

class SeekerModelThree(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
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

# -----------------------
# JOB SYSTEM (CLEAN SETUP)
# -----------------------

class Job(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)  # employer
    title = models.CharField(null=True, max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # NEW FIELD ⬇️
    interview_questions = models.TextField(
        blank=True,
        null=True,
        help_text="Enter one question per line."
    )

    created_at = models.DateTimeField(null=True,auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"



class JobRequirementOne(models.Model):
    job = models.OneToOneField(Job,null=True, on_delete=models.CASCADE, related_name='req_one')
    total_years_of_experience = models.IntegerField(null=True)
    html_experience = models.IntegerField(null=True)
    css_experience = models.IntegerField(null=True)


class JobRequirementTwo(models.Model):
    job = models.OneToOneField(Job, null=True,on_delete=models.CASCADE, related_name='req_two')
    python_experience = models.IntegerField(null=True)
    java_experience = models.IntegerField(null=True)
    javascript_experience = models.IntegerField(null=True)
    cplusplus_experience = models.IntegerField(null=True)
    csharp_experience = models.IntegerField(null=True)
    ruby_experience = models.IntegerField(null=True)


class JobRequirementThree(models.Model):
    job = models.OneToOneField(Job,null=True, on_delete=models.CASCADE, related_name='req_three')
    react_experience = models.IntegerField(null=True)
    vue_experience = models.IntegerField(null=True)
    angular_experience = models.IntegerField(null=True)
    django_experience = models.IntegerField(null=True)
    flask_experience = models.IntegerField(null=True)
    ruby_on_rails_experience = models.IntegerField(null=True)
    fastapi_experience = models.IntegerField(null=True)
    laravel_experience = models.IntegerField(null=True)
    express_experience = models.IntegerField(null=True)
    springboot_experience = models.IntegerField(null=True)
    aspnet_experience = models.IntegerField(null=True)
    oracle_experience = models.IntegerField(null=True)
    mysql_experience = models.IntegerField(null=True)
    sqlite_experience = models.IntegerField(null=True)
    mongodb_experience = models.IntegerField(null=True)
    postgresql_experience = models.IntegerField(null=True)



    
    


