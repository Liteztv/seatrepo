from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from .models import (
    EmployerCreditWallet, CreditTransaction,
    AccessPurchase, AccessLog, Profile
)
from django.contrib.auth.models import User


def get_or_create_wallet(employer: User):
    wallet, created = EmployerCreditWallet.objects.get_or_create(employer=employer)
    return wallet


def get_action_price(action: str) -> Decimal:
    """
    Map action -> price from settings.
    """
    mapping = {
        "message": getattr(settings, "HIRE_MESSAGE_PRICE", 0.00),
        "interview": getattr(settings, "HIRE_INTERVIEW_PRICE", 0.00),
        "resume": getattr(settings, "HIRE_RESUME_PRICE", 0.00),
        "hire": getattr(settings, "HIRE_HIRE_PRICE", 0.00),
    }
    return Decimal(mapping.get(action, 0.00))


def get_action_credits(action: str) -> int:
    mapping = {
        "message": getattr(settings, "CREDITS_PER_MESSAGE", 1),
        "interview": getattr(settings, "CREDITS_PER_INTERVIEW", 2),
        "resume": getattr(settings, "CREDITS_PER_RESUME", 1),
        "hire": getattr(settings, "CREDITS_PER_HIRE", 5),
    }
    return mapping.get(action, 1)


def seeker_allows_action(seeker: User, action: str) -> bool:
    """
    Enforce candidate opt-out settings.
    """
    profile = getattr(seeker, "profile", None)
    if not profile:
        return True  # no profile, default allow

    if action == "message":
        return profile.allow_messages
    if action == "interview":
        return profile.allow_interviews
    if action == "resume":
        return profile.allow_resume_view
    if action == "hire":
        return profile.allow_hire_requests
    return True

def has_access(employer: User, seeker: User, job, action: str) -> bool:
    """
    True if employer already has access for this action.
    Free-mode: always True.
    """
    price = get_action_price(action)
    if price == 0:
        return True

    return AccessPurchase.objects.filter(
        employer=employer,
        seeker=seeker,
        job=job,
        action=action,
        paid=True,
    ).exists()


def grant_free_access(employer, seeker, job, action):
    AccessPurchase.objects.get_or_create(
        employer=employer,
        seeker=seeker,
        job=job,
        action=action,
        defaults={
            "paid": True,
            "via_credits": False,
            "via_stripe": False,
            "price": Decimal("0.00"),
        },
    )
    AccessLog.objects.create(
        employer=employer,
        seeker=seeker,
        job=job,
        action=action,
    )


def consume_credits_or_fail(employer, seeker, job, action) -> bool:
    """
    Try to pay with credits. Returns True if successful.
    If not enough credits, returns False.
    """
    needed = get_action_credits(action)
    wallet = get_or_create_wallet(employer)

    if wallet.balance < needed:
        return False

    wallet.balance -= needed
    wallet.save()

    CreditTransaction.objects.create(
        wallet=wallet,
        amount=-needed,
        reason=f"{action} access for {seeker.username}",
    )

    AccessPurchase.objects.get_or_create(
        employer=employer,
        seeker=seeker,
        job=job,
        action=action,
        defaults={
            "paid": True,
            "via_credits": True,
            "price": get_action_price(action),
        },
    )

    AccessLog.objects.create(
        employer=employer,
        seeker=seeker,
        job=job,
        action=action,
    )

    return True
