from django.db import models
from django.contrib.auth.models import User


# ==========================
# USER PROFILE / ROLE SYSTEM
# ==========================
class Profile(models.Model):
    ROLE_CHOICES = (
        ("seeker", "Job Seeker"),
        ("employer", "Employer"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} – {self.role or 'No role'}"


# ====================
# SEEKER EXPERIENCE
# ====================
class SeekerModelOne(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    total_years_of_experience = models.IntegerField(default=0)
    html_experience = models.IntegerField(default=0)
    css_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Experience 1"


class SeekerModelTwo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    python_experience = models.IntegerField(default=0)
    java_experience = models.IntegerField(default=0)
    javascript_experience = models.IntegerField(default=0)
    cplusplus_experience = models.IntegerField(default=0)
    csharp_experience = models.IntegerField(default=0)
    ruby_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Experience 2"


class SeekerModelThree(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    react_experience = models.IntegerField(default=0)
    vue_experience = models.IntegerField(default=0)
    angular_experience = models.IntegerField(default=0)
    django_experience = models.IntegerField(default=0)
    flask_experience = models.IntegerField(default=0)
    ruby_on_rails_experience = models.IntegerField(default=0)
    fastapi_experience = models.IntegerField(default=0)
    laravel_experience = models.IntegerField(default=0)
    express_experience = models.IntegerField(default=0)
    springboot_experience = models.IntegerField(default=0)
    aspnet_experience = models.IntegerField(default=0)
    oracle_experience = models.IntegerField(default=0)
    mysql_experience = models.IntegerField(default=0)
    sqlite_experience = models.IntegerField(default=0)
    mongodb_experience = models.IntegerField(default=0)
    postgresql_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Experience 3"


# ====================
# JOB SYSTEM
# ====================
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Employer account

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, default="No description provided.")

    interview_questions = models.TextField(
        blank=True,
        help_text="Enter one question per line."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


# ============================
# JOB REQUIREMENTS (3 GROUPS)
# ============================
class JobRequirementOne(models.Model):
    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="req_one"
    )
    total_years_of_experience = models.IntegerField(default=0)
    html_experience = models.IntegerField(default=0)
    css_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"Req1 for {self.job.title}"


class JobRequirementTwo(models.Model):
    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="req_two"
    )
    python_experience = models.IntegerField(default=0)
    java_experience = models.IntegerField(default=0)
    javascript_experience = models.IntegerField(default=0)
    cplusplus_experience = models.IntegerField(default=0)
    csharp_experience = models.IntegerField(default=0)
    ruby_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"Req2 for {self.job.title}"


class JobRequirementThree(models.Model):
    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="req_three"
    )

    react_experience = models.IntegerField(default=0)
    vue_experience = models.IntegerField(default=0)
    angular_experience = models.IntegerField(default=0)
    django_experience = models.IntegerField(default=0)
    flask_experience = models.IntegerField(default=0)
    ruby_on_rails_experience = models.IntegerField(default=0)
    fastapi_experience = models.IntegerField(default=0)
    laravel_experience = models.IntegerField(default=0)
    express_experience = models.IntegerField(default=0)
    springboot_experience = models.IntegerField(default=0)
    aspnet_experience = models.IntegerField(default=0)
    oracle_experience = models.IntegerField(default=0)
    mysql_experience = models.IntegerField(default=0)
    sqlite_experience = models.IntegerField(default=0)
    mongodb_experience = models.IntegerField(default=0)
    postgresql_experience = models.IntegerField(default=0)

    def __str__(self):
        return f"Req3 for {self.job.title}"


# ====================
# INBOX + INTERVIEWS
# ====================
class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True, default="The body was not filled in.")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} ({self.sender} → {self.receiver})"


class InterviewAssignment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    employer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interview_assignments_sent"
    )
    seeker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interview_assignments_received"
    )
    questions = models.TextField()
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    employer_marked_hire = models.BooleanField(default=False)
    superuser_notified = models.BooleanField(default=False)

    def __str__(self):
        return f"Interview for {self.seeker.username} – {self.job.title}"


class InterviewResponse(models.Model):
    assignment = models.ForeignKey(
        InterviewAssignment, on_delete=models.CASCADE, related_name="responses"
    )
    seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    video = models.FileField(upload_to="interview_videos/")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.seeker.username} – {self.assignment.job.title}"
