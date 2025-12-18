# liteapp/utils.py (create this file)
from .models import Profile, Conversation, EmployerAccess, Job
from django.conf import settings
from django.contrib.auth.models import User

def get_user_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile


def get_or_create_conversation(user_a, user_b, job=None):
    convo = Conversation.objects.filter(
        user1__in=[user_a, user_b],
        user2__in=[user_a, user_b],
        job=job
    ).first()

    if convo:
        return convo

    # Create a new one
    return Conversation.objects.create(
        user1=user_a,
        user2=user_b,
        job=job
    )


def _has_access(employer, seeker, job, access_type, price):
    if price == 0:
        return True

    return EmployerAccess.objects.filter(
        employer=employer,
        seeker=seeker,
        job=job,
        access_type=access_type,
        paid=True
    ).exists()


def has_interview_access(employer, seeker, job):
    from django.conf import settings
    from .models import EmployerAccess

    # ❌ REMOVE auto-grant based on price
    return EmployerAccess.objects.filter(
        employer=employer,
        seeker=seeker,
        job=job,
        access_type="interview",
        paid=True,
    ).exists()



def has_resume_access(employer, seeker, job):
    return EmployerAccess.objects.filter(
        employer=employer,
        seeker=seeker,
        job=job,
        access_type="resume",
        paid=True,
    ).exists()


def has_hire_access(employer, seeker, job):
    return EmployerAccess.objects.filter(
        employer=employer,
        seeker=seeker,
        job=job,
        access_type="hire",
        paid=True,
    ).exists()

def match_software_seekers(job):
    # uses SeekerModelOne/Two/Three
    pass

def match_machinist_seekers(job):
    # uses MachinistExperience
    pass

def match_seekers_for_job(job):
    if job.job_type == Job.SOFTWARE:
        return match_software_seekers(job)
    elif job.job_type == Job.MACHINIST:
        return match_machinist_seekers(job)
    return User.objects.none()


