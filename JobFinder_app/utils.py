# liteapp/utils.py (create this file)
from .models import Profile

def get_user_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile
