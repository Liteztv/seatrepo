from django.db.models import Q, IntegerField

def dynamic_match(seeker_obj, employer_model):
    q_filters = Q()

    for field in employer_model._meta.get_fields():
        if isinstance(field, IntegerField):
            name = field.name
            seeker_value = getattr(seeker_obj, name, None)

            if seeker_value is None or seeker_value <= 0:
                continue

            q_filters &= (
                Q(**{f"{name}__lte": seeker_value}) |
                Q(**{f"{name}__isnull": True})
            )

    if not q_filters.children:
        return employer_model.objects.none()

    return employer_model.objects.filter(q_filters)
