from django.urls import reverse
from django.http import FileResponse, Http404
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ( SeekerFormOne, SeekerFormTwo, SeekerFormThree, RegistrationForm, LoginForm,
                    JobForm, JobRequirementOneForm, JobRequirementTwoForm, JobRequirementThreeForm, ResumeUploadForm,
                    EmailChangeForm, ConfirmDeleteForm, MachinistJobRequirementForm, MachinistExperienceForm
                    )
# from django.urls import reverse
from .models import ( SeekerModelOne, SeekerModelThree, SeekerModelTwo, Profile, 
                     Job, JobRequirementOne, JobRequirementTwo, JobRequirementThree,
                     InterviewAssignment, InterviewResponse, Message, Conversation, SeekerResume, EmployerAccess,
                     MachinistExperience,
                     )

from django.db import transaction
from .utils import has_hire_access, has_interview_access, has_resume_access
from django.conf import settings

def get_or_create_conversation(user1, user2, job=None):
    convo = Conversation.objects.filter(
        Q(user1=user1, user2=user2) |
        Q(user1=user2, user2=user1)
    ).first()

    if convo:
        return convo

    with transaction.atomic():
        convo = Conversation.objects.create(
            user1=user1,
            user2=user2,
            job=job
        )
        print("✅ Conversation CREATED:", convo.id)

    return convo


def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Ensure only the employer who created the job can edit it
    if job.user != request.user:
        return redirect("employer_dashboard")

    req1 = job.req_one
    req2 = job.req_two
    req3 = job.req_three

    if request.method == "POST":
        job_form = JobForm(request.POST, instance=job)
        req1_form = JobRequirementOneForm(request.POST, instance=req1)
        req2_form = JobRequirementTwoForm(request.POST, instance=req2)
        req3_form = JobRequirementThreeForm(request.POST, instance=req3)

        if job_form.is_valid() and req1_form.is_valid() and req2_form.is_valid() and req3_form.is_valid():
            job_form.save()
            req1_form.save()
            req2_form.save()
            req3_form.save()

            return redirect("employer_dashboard")

    else:
        job_form = JobForm(instance=job)
        req1_form = JobRequirementOneForm(instance=req1)
        req2_form = JobRequirementTwoForm(instance=req2)
        req3_form = JobRequirementThreeForm(instance=req3)

    return render(request, "JobFinder_app/edit_job.html", {
        "job_form": job_form,
        "req1_form": req1_form,
        "req2_form": req2_form,
        "req3_form": req3_form,
        "job": job,
    })

def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only the employer who created the job may delete it
    if job.user != request.user:
        return redirect("employer_dashboard")

    if request.method == "POST":
        job.delete()
        return redirect("employer_dashboard")

    return render(request, "JobFinder_app/delete_job.html", {"job": job})

@login_required
def create_job_select_type(request):
    return render(request, "JobFinder_app/create_job_select_type.html")


@login_required
def create_job_machinist(request):
    if request.method == "POST":
        job_form = JobForm(request.POST)
        req_form = MachinistJobRequirementForm(request.POST)

        if job_form.is_valid() and req_form.is_valid():
            job = job_form.save(commit=False)
            job.user = request.user
            job.job_type = Job.MACHINIST
            job.save()

            req = req_form.save(commit=False)
            req.job = job
            req.save()

            return redirect("employer_dashboard")
    else:
        job_form = JobForm()
        req_form = MachinistJobRequirementForm()

    return render(request, "JobFinder_app/create_job_machinist.html", {
        "job_form": job_form,
        "req_form": req_form,
    })


def create_job_software(request):
    if request.method == "POST":
        job_form = JobForm(request.POST)
        req1_form = JobRequirementOneForm(request.POST)
        req2_form = JobRequirementTwoForm(request.POST)
        req3_form = JobRequirementThreeForm(request.POST)
        job.job_type = Job.SOFTWARE

        if job_form.is_valid() and req1_form.is_valid() and req2_form.is_valid() and req3_form.is_valid():

            job = job_form.save(commit=False)
            job.user = request.user
            job.save()

            req1 = req1_form.save(commit=False)
            req1.job = job
            req1.save()

            req2 = req2_form.save(commit=False)
            req2.job = job
            req2.save()

            req3 = req3_form.save(commit=False)
            req3.job = job
            req3.save()

            return redirect("employer_dashboard")

    else:
        job_form = JobForm()
        req1_form = JobRequirementOneForm()
        req2_form = JobRequirementTwoForm()
        req3_form = JobRequirementThreeForm()

    return render(request, "JobFinder_app/create_job.html", {
        "job_form": job_form,
        "req1_form": req1_form,
        "req2_form": req2_form,
        "req3_form": req3_form,
    })

@login_required
def create_job_choice(request):
    return render(request, "JobFinder_app/create_job_choice.html")


def match_seekers_for_job(job):
    req1 = job.req_one
    req2 = job.req_two
    req3 = job.req_three

    seekers1 = SeekerModelOne.objects.all()
    seekers2 = SeekerModelTwo.objects.all()
    seekers3 = SeekerModelThree.objects.all()

    # Req1
    filters_1 = {}
    for field in ["total_years_of_experience", "html_experience", "css_experience"]:
        val = getattr(req1, field)
        if val and val > 0:
            filters_1[f"{field}__gte"] = val
    seekers1 = seekers1.filter(**filters_1)

    # Req2
    fields2 = ["python_experience","java_experience","javascript_experience","cplusplus_experience","csharp_experience","ruby_experience"]
    filters_2 = {}
    for field in fields2:
        val = getattr(req2, field)
        if val and val > 0:
            filters_2[f"{field}__gte"] = val
    seekers2 = seekers2.filter(**filters_2)

    # Req3
    fields3 = [f.name for f in JobRequirementThree._meta.fields if f.name not in ("id", "job")]
    filters_3 = {}
    for field in fields3:
        val = getattr(req3, field)
        if val and val > 0:
            filters_3[f"{field}__gte"] = val
    seekers3 = seekers3.filter(**filters_3)

    ids = (
        set(seekers1.values_list("user", flat=True)) &
        set(seekers2.values_list("user", flat=True)) &
        set(seekers3.values_list("user", flat=True))
    )

    return User.objects.filter(id__in=ids)


def employer_dashboard(request):
    jobs = Job.objects.filter(user=request.user).order_by("-created_at")

    job_data = []
    for job in jobs:
        seekers_qs = match_seekers_for_job(job)

        open_candidates = []
        interviewed_candidates = []
        

        for idx, seeker in enumerate(seekers_qs, start=1):
            # latest assignment for this job+seeker, if any
            assignment = (
                InterviewAssignment.objects
                .filter(job=job, seeker=seeker)
                .order_by("-assigned_at")
                .first()
            )
            resume_obj = SeekerResume.objects.filter(
                user=seeker,
                resume__isnull=False
            ).exclude(resume="").first()

            resume_exists= SeekerResume.objects.filter(
                user=seeker,
                resume__isnull=False
            ).exclude(resume="").first()

            resume_file = resume_obj.resume if resume_obj else None

            base = {
                "label": f"Candidate #{idx}",
                "user_id": seeker.id,
                "match_percentage": 85,  # stub; you can compute a real score later
                "assignment_id": assignment.id if assignment else None,
                "has_assignment": assignment is not None,
                "completed": assignment.completed if assignment else False,
                "resume_file": resume_file,
                "has_resume": resume_exists,
                "can_interview": has_interview_access(request.user, seeker, job),
                "can_view_resume": has_resume_access(request.user, seeker, job),
                "can_hire": has_hire_access(request.user, seeker, job),
                "interview_sent": bool(assignment),
            }

            if assignment and assignment.completed:
                interviewed_candidates.append(base)
            elif assignment:
                base["interview_sent"] = True
                open_candidates.append(base)
            else:
                base["interview_sent"] = False
                open_candidates.append(base)

        job_data.append({
            "job": job,
            "candidates": open_candidates,
            "interviewed_candidates": interviewed_candidates,
        })

    return render(request, "JobFinder_app/employer_dashboard.html", {
        "job_data": job_data
    })

def seeker_dashboard(request):
    assignments = InterviewAssignment.objects.filter(seeker=request.user).order_by("-assigned_at")
    messages = Message.objects.filter(receiver=request.user).order_by("-created_at")

    return render(request, "JobFinder_app/seeker_dashboard.html", {
        "assignments": assignments,
        "messages": messages,
    })

def home_view(request):
    return render(request,'JobFinder_app/home.html')

def seeker_view(request):
    if request.method == 'POST':
        form = SeekerFormOne(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)
            return redirect('seekerviewtwo')

    else:
        form = SeekerFormOne()
        return render(request,'JobFinder_app/seekerex.html',context={'form': form})
    
def seekertwo_view(request):

    if request.method == 'POST':
        form = SeekerFormTwo(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)
            return redirect('seekerviewthree')

    else:
        form = SeekerFormTwo()
        return render(request,'JobFinder_app/seekerextwo.html',context={'form': form})
    
def seekerthree_view(request):
    if request.method == 'POST':
        form = SeekerFormThree(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)
            return render(request,'JobFinder_app/thanks.html')

    else:
        form = SeekerFormThree()
        return render(request,'JobFinder_app/seekerexthree.html',context={'form': form})
    
@login_required
def machinist_experience_view(request):
    try:
        instance = MachinistExperience.objects.get(user=request.user)
    except MachinistExperience.DoesNotExist:
        instance = None

    if request.method == "POST":
        form = MachinistExperienceForm(request.POST, instance=instance)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect("seeker_dashboard")
        else:
            print("❌ FORM ERRORS:", form.errors)

    else:
        form = MachinistExperienceForm(instance=instance)

    return render(request, "JobFinder_app/machinist_experience.html", {
        "form": form
    })



def thanks_view(request):
    return render(request,'JobFinder_app/thanks.html')

def employer_view(request):
    return render(request, 'JobFinder_app/employerhome.html')


def employer_experience_view(request):
    return render(request, 'JobFinder_app/employerexone.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("role_redirect")
            else:
                # Password or username wrong → show an error
                return render(request, "JobFinder_app/login.html", {
                    "form": form,
                    "error": "Invalid username or password."
                })
    else:
        form = LoginForm()

    return render(request, "JobFinder_app/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Explicitly create or update Profile with chosen role
            role = form.cleaned_data["role"]
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()

            login(request, user)
            return redirect("role_redirect")
    else:
        form = RegistrationForm()

    return render(request, "JobFinder_app/registration.html", {"form": form})


from .utils import get_user_profile

def role_redirect(request):
    profile = get_user_profile(request.user)  # never raises RelatedObjectDoesNotExist

    if profile.role == "employer":
        return redirect("employer_dashboard")
    elif profile.role == "seeker":
        return redirect("seeker_dashboard")
    else:
        # Fallback: if role missing, send to landing or let them choose
        return redirect("landing")

    
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def seeker_form_one(request):
    instance, _ = SeekerModelOne.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = SeekerFormOne(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("seeker_form2")
    else:
        form = SeekerFormOne(instance=instance)

    return render(request, "JobFinder_app/seeker_form1.html", {
        "form": form,
        "edit_mode": True,
    })


@login_required
def seeker_form_two(request):
    instance, _ = SeekerModelTwo.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = SeekerFormTwo(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("seeker_form3")
    else:
        form = SeekerFormTwo(instance=instance)

    return render(request, "JobFinder_app/seeker_form2.html", {
        "form": form,
        "edit_mode": True,
    })



@login_required
def seeker_form_three(request):
    instance, _ = SeekerModelThree.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = SeekerFormThree(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("seeker_dashboard")
    else:
        form = SeekerFormThree(instance=instance)

    return render(request, "JobFinder_app/seeker_form3.html", {
        "form": form,
        "edit_mode": True,
    })



def landing_view(request):
    return render(request, "JobFinder_app/landing.html")





@login_required
def send_interview(request, job_id, seeker_id):
    job = get_object_or_404(Job, id=job_id)
    seeker = get_object_or_404(User, id=seeker_id)

    if job.user != request.user:
        messages.error(request, "Not authorized.")
        return redirect("employer_dashboard")

    if not job.interview_questions:
        messages.error(request, "No interview questions.")
        return redirect("employer_dashboard")

    # ✅ Get or create conversation
    conversation = Conversation.objects.filter(
        Q(user1=request.user, user2=seeker) |
        Q(user1=seeker, user2=request.user)
    ).first()

    if not has_interview_access(request.user, seeker, job):
        messages.error(
        request,
        "Purchase interview access to send questions."
        )
        return redirect("employer_dashboard")


    if not conversation:
        conversation = Conversation.objects.create(
            user1=request.user,
            user2=seeker,
            job=job,
        )

    assignment, created = InterviewAssignment.objects.get_or_create(
        job=job,
        employer=request.user,
        seeker=seeker,
        defaults={"questions": job.interview_questions},
    )

    interview_link = request.build_absolute_uri(
        reverse("answer_interview", args=[assignment.id])
    )

    # ✅ Message MUST link to conversation
    Message.objects.create(
        conversation=conversation,
        sender=request.user,
        receiver=seeker,
        subject=f"Interview for {job.title}",
        body=f"You have been invited to complete a video interview.\n\n"
            f"Click here to begin:\n{interview_link}l",
        job=job,
    )

    messages.success(request, "Interview sent.")
    return redirect("employer_dashboard")


@login_required(login_url="login")
def inbox_view(request):
    user = request.user

    messages_qs = Message.objects.filter(receiver=user).order_by("-created_at")

    # Interviews where this user is the seeker (to answer)
    assignments_to_answer = InterviewAssignment.objects.filter(
        seeker=user, completed=False
    ).order_by("-assigned_at")

    # Interviews completed for jobs this employer owns
    assignments_for_review = InterviewAssignment.objects.filter(
        employer=user, completed=True
    ).order_by("-assigned_at")

    return render(request, "JobFinder_app/inbox.html", {
        "messages": messages_qs,
        "assignments_to_answer": assignments_to_answer,
        "assignments_for_review": assignments_for_review,
        "unread_count": messages.filter(is_read=False).count(),
    })
 
@login_required(login_url="login")
def view_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, receiver=request.user)

    # Mark as read
    if not msg.is_read:
        msg.is_read = True
        msg.save()

    return render(request, "JobFinder_app/message_detail.html", {
        "msg": msg
    })


@login_required
@require_http_methods(["GET", "POST"])
def answer_interview(request, assignment_id):
    assignment = get_object_or_404(InterviewAssignment, id=assignment_id)

    # only the seeker assigned may answer
    if assignment.seeker != request.user:
        return redirect("inbox_pro")

    questions = [q.strip() for q in assignment.questions.splitlines() if q.strip()]

    if request.method == "POST":
        # clear any existing responses for re-tries, if you want
        assignment.responses.all().delete()

        for idx, question in enumerate(questions):
            file_key = f"video_{idx}"
            video_file = request.FILES.get(file_key)
            if video_file:
                InterviewResponse.objects.create(
                    assignment=assignment,
                    seeker=request.user,
                    question=question,
                    video=video_file,
                )

        assignment.completed = True
        assignment.save()

        # notify employer in inbox
        Message.objects.create(
            sender=request.user,
            receiver=assignment.employer,
            subject=f"Interview Completed for {assignment.job.title}",
            body="The candidate has completed their video interview.",
            job=assignment.job,
        )

        return redirect("inbox_pro")

    return render(request, "JobFinder_app/answer_interview.html", {
        "assignment": assignment,
        "questions": questions,
    })

@login_required
def hire_from_assignment(request, assignment_id):
    assignment = get_object_or_404(InterviewAssignment, id=assignment_id)

    if assignment.employer != request.user:
        return redirect("employer_dashboard")

    assignment.employer_marked_hire = True
    assignment.save()

    # notify superusers so they can connect them
    superusers = User.objects.filter(is_superuser=True)
    for admin in superusers:
        Message.objects.create(
            sender=request.user,
            receiver=admin,
            subject="Candidate ready to hire",
            body=(
                f"Employer {request.user.username} wants to hire "
                f"{assignment.seeker.username} for job '{assignment.job.title}'."
            ),
            job=assignment.job,
        )

    assignment.superuser_notified = True
    assignment.save()

    messages.success(request, "Candidate marked for hire.")
    return redirect("employer_dashboard")


@login_required
def inbox_pro(request):
    unread_count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).order_by("-created_at")

    convo_id = request.GET.get("c")
    active_conversation = None

    if convo_id:
        active_conversation = get_object_or_404(
            conversations, id=convo_id
        )

        # ✅ MARK MESSAGES AS READ
        Message.objects.filter(
            conversation=active_conversation,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

    return render(request, "JobFinder_app/inbox_pro.html", {
        "conversations": conversations,
        "active_conversation": active_conversation,
        "unread_count": unread_count,
    })

@login_required
def conversation_view(request, convo_id):
    convo = get_object_or_404(Conversation, id=convo_id)

    # ✅ Must be a participant
    if request.user not in (convo.user1, convo.user2):
        return redirect("inbox_pro")

    # ✅ Identify the OTHER user
    other_user = convo.user2 if request.user == convo.user1 else convo.user1

    # ✅ BLOCK EMPLOYER FROM SENDING UNLESS HIRED / PAID
    if request.method == "POST":
        if request.user.profile.role == "employer":
            if not has_hire_access(request.user, other_user, convo.job):
                messages.error(
                    request,
                    "You must hire this candidate before sending messages."
                )
                return redirect("conversation_view", convo_id=convo.id)

        msg = request.POST.get("message", "").strip()
        if msg:
            Message.objects.create(
                conversation=convo,
                sender=request.user,
                receiver=other_user,
                body=msg,
                job=convo.job,
            )

    # ✅ Mark received messages as read (DO NOT gate this)
    Message.objects.filter(
        conversation=convo,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    # ✅ Load conversations list
    conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).distinct()

    return render(request, "JobFinder_app/inbox_pro.html", {
        "conversations": conversations,
        "active_conversation": convo,
    })


@login_required
def review_interview(request, assignment_id):
    assignment = get_object_or_404(InterviewAssignment, id=assignment_id)

    # Security: only the employer who sent it can view
    if assignment.employer != request.user:
        return redirect("employer_dashboard")

    responses = assignment.responses.all().order_by("id")

    return render(request, "JobFinder_app/review_interview.html", {
        "assignment": assignment,
        "responses": responses,
    })

@login_required
def upload_resume(request):
    instance, _ = SeekerResume.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("seeker_dashboard")
    else:
        form = ResumeUploadForm(instance=instance)

    return render(request, "JobFinder_app/upload_resume.html", {
        "form": form
    })

@login_required
def view_resume(request, job_id, seeker_id):
    """
    Open a seeker's resume INLINE in the browser.
    Only employers with resume access may view.
    """

    # ✅ Only employers allowed
    if request.user.profile.role != "employer":
        raise Http404()

    # ✅ Job must belong to employer
    job = get_object_or_404(Job, id=job_id, user=request.user)

    # ✅ Find resume safely
    resume_obj = (
        SeekerResume.objects
        .filter(user_id=seeker_id)
        .exclude(resume="")
        .exclude(resume__isnull=True)
        .first()
    )

    if not resume_obj or not resume_obj.resume:
        messages.error(request, "This candidate has not uploaded a resume.")
        return redirect("employer_dashboard")

    # ✅ PAYWALL ENFORCEMENT (CRITICAL)
    if not has_resume_access(request.user, resume_obj.user, job):
        messages.error(
            request,
            "You must unlock resume access to view this document."
        )
        return redirect("employer_dashboard")

    try:
        response = FileResponse(
            resume_obj.resume.open("rb"),
            content_type="application/pdf"
        )

        # ✅ FORCE INLINE VIEWING (NOT DOWNLOAD)
        filename = resume_obj.resume.name.split("/")[-1]
        response["Content-Disposition"] = f'inline; filename="{filename}"'

        return response

    except Exception:
        raise Http404("Unable to open resume")

@login_required
def account_settings(request):
    return render(request, "JobFinder_app/account_settings.html")


@login_required
def change_email(request):
    form = EmailChangeForm(request.POST or None, instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Email updated successfully.")
        return redirect("account_settings")

    return render(request, "JobFinder_app/change_email.html", {"form": form})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password changed successfully.")
        return redirect("account_settings")

    return render(request, "JobFinder_app/change_password.html", {"form": form})


@login_required
def delete_account(request):
    form = ConfirmDeleteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("landing")

    return render(request, "JobFinder_app/delete_account.html", {"form": form})


@login_required
def purchase_hire_access(request, job_id, seeker_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    seeker = get_object_or_404(User, id=seeker_id)

    access, created = EmployerAccess.objects.get_or_create(
        employer=request.user,
        seeker=seeker,
        job=job,
        defaults={"paid": True}
    )

    if not created:
        access.paid = True
        access.save()

    messages.success(
        request,
        "Hire access granted. You may now message this candidate."
    )

    return redirect("employer_dashboard")

def purchase_interview_access(request, job_id, seeker_id):
    return _purchase_access(request, job_id, seeker_id, "interview", settings.INTERVIEW_ACCESS_PRICE)

def purchase_resume_access(request, job_id, seeker_id):
    return _purchase_access(request, job_id, seeker_id, "resume", settings.RESUME_ACCESS_PRICE)

def purchase_hire_access(request, job_id, seeker_id):
    return _purchase_access(request, job_id, seeker_id, "hire", settings.HIRE_ACCESS_PRICE)

def _purchase_access(request, job_id, seeker_id, access_type, price):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    seeker = get_object_or_404(User, id=seeker_id)

    EmployerAccess.objects.update_or_create(
        employer=request.user,
        seeker=seeker,
        job=job,
        access_type=access_type,
        defaults={"paid": True, "price": price},
    )

    messages.success(request, f"{access_type.capitalize()} access granted.")
    return redirect("employer_dashboard")

@login_required
def buy_credits(request):
    """
    Placeholder for Stripe / credit purchase page.
    Currently free or $0 mode.
    """
    messages.info(request, "Credits system coming soon. Currently free mode.")
    return redirect("account_settings")


@login_required
def purchase_interview_access(request, job_id, seeker_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    seeker = get_object_or_404(User, id=seeker_id)

    EmployerAccess.objects.update_or_create(
        employer=request.user,
        seeker=seeker,
        job=job,
        access_type="interview",
        defaults={
            "paid": True,
            "price": settings.INTERVIEW_ACCESS_PRICE,
        }
    )

    messages.success(request, "Interview unlocked.")
    return redirect("employer_dashboard")


@login_required
def purchase_resume_access(request, job_id, seeker_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    seeker = get_object_or_404(User, id=seeker_id)

    EmployerAccess.objects.update_or_create(
        employer=request.user,
        seeker=seeker,
        job=job,
        access_type="resume",
        defaults={
            "paid": True,
            "price": settings.RESUME_ACCESS_PRICE,
        }
    )

    messages.success(request, "Resume access unlocked.")
    return redirect("employer_dashboard")



@login_required
def purchase_hire_access(request, job_id, seeker_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    seeker = get_object_or_404(User, id=seeker_id)

    EmployerAccess.objects.update_or_create(
        employer=request.user,
        seeker=seeker,
        job=job,
        access_type="hire",
        defaults={
            "paid": True,
            "price": settings.HIRE_ACCESS_PRICE,
        }
    )

    messages.success(request, "Hire access unlocked.")
    return redirect("employer_dashboard")

@login_required
def candidate_summary(request, job_id, seeker_id):
    """
    Employer-only anonymous candidate skill summary.
    Shows only skills with > 0 experience.
    """

    # ✅ Ensure job belongs to employer
    job = get_object_or_404(Job, id=job_id, user=request.user)

    # ✅ Fetch seeker experience models safely
    sm1 = SeekerModelOne.objects.filter(user_id=seeker_id).first()
    sm2 = SeekerModelTwo.objects.filter(user_id=seeker_id).first()
    sm3 = SeekerModelThree.objects.filter(user_id=seeker_id).first()

    if not any([sm1, sm2, sm3]):
        raise Http404("Candidate data not found")

    skills = []

    def extract_skills(instance, exclude=("id", "user", "first_name", "last_name")):
        if not instance:
            return
        for field in instance._meta.fields:
            name = field.name
            if name in exclude:
                continue
            value = getattr(instance, name)
            if isinstance(value, int) and value > 0:
                skills.append({
                    "name": name.replace("_", " ").title(),
                    "years": value,
                })

    extract_skills(sm1)
    extract_skills(sm2)
    extract_skills(sm3)

    total_years = sm1.total_years_of_experience if sm1 else None

    return render(request, "JobFinder_app/candidate_summary.html", {
        "job": job,
        "seeker_id": seeker_id,
        "total_years": total_years,
        "skills": skills,
    })