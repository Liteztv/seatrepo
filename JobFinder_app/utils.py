# liteapp/utils.py (create this file)
from .models import Profile, Conversation

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
