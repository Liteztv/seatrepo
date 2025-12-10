from django.contrib import admin
from .models import (
    Profile,
    SeekerModelOne, SeekerModelTwo, SeekerModelThree,
    Job, JobRequirementOne, JobRequirementTwo, JobRequirementThree,
    Message, InterviewAssignment, InterviewResponse, 
)

# EmployerCreditWallet,
#     CreditTransaction, AccessLog, AccessPurchase

admin.site.register(SeekerModelOne)
admin.site.register(SeekerModelTwo)
admin.site.register(SeekerModelThree)
admin.site.register(Message)
admin.site.register(InterviewAssignment)
admin.site.register(InterviewResponse)
# admin.site.register(EmployerCreditWallet)
# admin.site.register(CreditTransaction)
# admin.site.register(AccessLog)
# admin.site.register(AccessPurchase)

class JobRequirementOneInline(admin.StackedInline):
    model = JobRequirementOne
    extra = 0

class JobRequirementTwoInline(admin.StackedInline):
    model = JobRequirementTwo
    extra = 0

class JobRequirementThreeInline(admin.StackedInline):
    model = JobRequirementThree
    extra = 0


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")
    search_fields = ("title", "user__username")
    list_filter = ("created_at",)

    inlines = [
        JobRequirementOneInline,
        JobRequirementTwoInline,
        JobRequirementThreeInline,
    ]
