# liteapp/utils.py (create this file)
from .models import Profile, Conversation, EmployerAccess
from django.conf import settings

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
    return _has_access(
        employer, seeker, job, "interview", settings.INTERVIEW_ACCESS_PRICE
    )


def has_resume_access(employer, seeker, job):
    return _has_access(
        employer, seeker, job, "resume", settings.RESUME_ACCESS_PRICE
    )


def has_hire_access(employer, seeker, job):
    return _has_access(
        employer, seeker, job, "hire", settings.HIRE_ACCESS_PRICE
    )