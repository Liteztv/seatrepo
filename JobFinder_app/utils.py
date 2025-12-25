# liteapp/utils.py (create this file)
from .models import ( Profile, Conversation, EmployerAccess, Job, SeekerModelOne, SeekerModelThree, SeekerModelTwo,
                     MachinistExperience
                     )
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
    
    try:
        req1 = job.req_one
        req2 = job.req_two
        req3 = job.req_three
    except Exception:
        return User.objects.none()

    seekers1 = SeekerModelOne.objects.all()
    seekers2 = SeekerModelTwo.objects.all()
    seekers3 = SeekerModelThree.objects.all()

    # Req1
    filters_1 = {
        f"{field}__gte": getattr(req1, field)
        for field in ["total_years_of_experience", "html_experience", "css_experience"]
        if getattr(req1, field) and getattr(req1, field) > 0
    }
    seekers1 = seekers1.filter(**filters_1)

    # Req2
    fields2 = [
        "python_experience", "java_experience", "javascript_experience",
        "cplusplus_experience", "csharp_experience", "ruby_experience"
    ]
    filters_2 = {
        f"{field}__gte": getattr(req2, field)
        for field in fields2
        if getattr(req2, field) and getattr(req2, field) > 0
    }
    seekers2 = seekers2.filter(**filters_2)

    # Req3
    fields3 = [
        f.name for f in req3._meta.fields
        if f.name not in ("id", "job")
    ]
    filters_3 = {
        f"{field}__gte": getattr(req3, field)
        for field in fields3
        if getattr(req3, field) and getattr(req3, field) > 0
    }
    seekers3 = seekers3.filter(**filters_3)

    ids = (
        set(seekers1.values_list("user_id", flat=True)) &
        set(seekers2.values_list("user_id", flat=True)) &
        set(seekers3.values_list("user_id", flat=True))
    )

    return User.objects.filter(id__in=ids)


def match_machinist_seekers(job):
    try:
        req = job.machinist_requirements
    except Exception:
        return User.objects.none()

    qs = MachinistExperience.objects.all()

    filters = {
        f"{field}__gte": getattr(req, field)
        for field in [
            "years_experience",
            "cnc_milling",
            "cnc_turning",
            "manual_lathe",
            "manual_mill",
            "welding",
            "fabrication",
            "minimum_hourly_pay",
        ]
        if getattr(req, field) and getattr(req, field) > 0
    }

    qs = qs.filter(**filters)

    return User.objects.filter(
        id__in=qs.values_list("user_id", flat=True)
    )


def match_seekers_for_job(job):
    if job.job_type == Job.SOFTWARE:
        return match_software_seekers(job)
    elif job.job_type == Job.MACHINIST:
        return match_machinist_seekers(job)
    return User.objects.none()


def calculate_match_percentage(job, seeker):
    """
    Returns a percentage (0–100) based on how many required fields
    the seeker meets or exceeds.
    """

    total_requirements = 0
    met_requirements = 0

    if job.job_type == Job.SOFTWARE:
        reqs = [
            (job.req_one, SeekerModelOne),
            (job.req_two, SeekerModelTwo),
            (job.req_three, SeekerModelThree),
        ]

        for req, seeker_model in reqs:
            seeker_exp = seeker_model.objects.filter(user=seeker).first()
            if not req or not seeker_exp:
                continue

            for field in req._meta.fields:
                if field.name in ("id", "job"):
                    continue

                required_val = getattr(req, field.name)
                if required_val and required_val > 0:
                    total_requirements += 1
                    seeker_val = getattr(seeker_exp, field.name, 0) or 0
                    if seeker_val >= required_val:
                        met_requirements += 1

    elif job.job_type == Job.MACHINIST:
        req = job.machinist_requirements
        seeker_exp = MachinistExperience.objects.filter(user=seeker).first()

        if req and seeker_exp:
            for field in req._meta.fields:
                if field.name in ("id", "job"):
                    continue

                required_val = getattr(req, field.name)
                if required_val and required_val > 0:
                    total_requirements += 1
                    seeker_val = getattr(seeker_exp, field.name, 0) or 0
                    if seeker_val >= required_val:
                        met_requirements += 1

    if total_requirements == 0:
        return 0

    return round((met_requirements / total_requirements) * 100)