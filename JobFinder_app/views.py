from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import ( SeekerFormOne, SeekerFormTwo, SeekerFormThree, RegistrationForm, LoginForm,
                    JobForm, JobRequirementOneForm, JobRequirementTwoForm, JobRequirementThreeForm,
                    )
# from django.urls import reverse
from .models import ( SeekerModelOne, SeekerModelThree, SeekerModelTwo, Profile, 
                     Job, JobRequirementOne, JobRequirementTwo, JobRequirementThree,
                     InterviewAssignment, InterviewResponse, Message, Conversation
                     )

def get_or_create_conversation(user1, user2):
    convo = Conversation.objects.filter(
        Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
    ).first()

    if convo:
        return convo

    return Conversation.objects.create(user1=user1, user2=user2)

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


def create_job(request):
    if request.method == "POST":
        job_form = JobForm(request.POST)
        req1_form = JobRequirementOneForm(request.POST)
        req2_form = JobRequirementTwoForm(request.POST)
        req3_form = JobRequirementThreeForm(request.POST)

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

            base = {
                "label": f"Candidate #{idx}",
                "user_id": seeker.id,
                "match_percentage": 85,  # stub; you can compute a real score later
                "assignment_id": assignment.id if assignment else None,
                "has_assignment": assignment is not None,
                "completed": assignment.completed if assignment else False,
            }

            if assignment and assignment.completed:
                interviewed_candidates.append(base)
            else:
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

def seeker_form_one(request):
    form = SeekerFormOne(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("seeker_form2")
    return render(request, "JobFinder_app/seeker_form1.html", {"form": form})


def seeker_form_two(request):
    form = SeekerFormTwo(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("seeker_form3")
    return render(request, "JobFinder_app/seeker_form2.html", {"form": form})


def seeker_form_three(request):
    form = SeekerFormThree(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("seeker_dashboard")
    return render(request, "JobFinder_app/seeker_form3.html", {"form": form})



def landing_view(request):
    return render(request, "JobFinder_app/landing.html")





@login_required
def send_interview(request, job_id, seeker_id):
    job = get_object_or_404(Job, id=job_id)
    seeker = get_object_or_404(User, id=seeker_id)

    # Security: Only job owner can send interviews
    if job.user != request.user:
        messages.error(request, "You do not have permission to send an interview for this job.")
        return redirect("employer_dashboard")

    # Validation: Ensure job has real interview questions
    if not job.interview_questions.strip() or job.interview_questions.strip() == "No interview questions provided.":
        messages.error(request, "This job has no interview questions yet.")
        return redirect("employer_dashboard")

    # Create or reuse existing assignment
    assignment, created = InterviewAssignment.objects.get_or_create(
        job=job,
        employer=request.user,
        seeker=seeker,
        defaults={"questions": job.interview_questions},
    )

    if not created:
        messages.info(request, "Interview already sent to this candidate.")
        return redirect("employer_dashboard")

    # ✅ Create or find the conversation
    convo = get_or_create_conversation(request.user, seeker)

    # ✅ Create inbox message tied to conversation
    Message.objects.create(
        sender=request.user,
        receiver=seeker,
        conversation=convo,
        subject=f"Interview for {job.title}",
        body="You have been invited to complete a video interview.",
        job=job,
    )

    messages.success(request, "Interview sent successfully!")
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
        return redirect("inbox")

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

        return redirect("inbox")

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

    return redirect("employer_dashboard")

@login_required(login_url="login")
def inbox_pro(request):
    # Get all conversations where the user is a participant
    conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).distinct()

    active_conversation = None

    # If "conversation_id" is provided, load that conversation
    convo_id = request.GET.get("c")
    if convo_id:
        active_conversation = get_object_or_404(
            Conversation,
            
            # Make sure the user is part of it
            Q(user1=request.user) | Q(user2=request.user),
            id=convo_id
        )

    return render(request, "JobFinder_app/inbox_pro.html", {
        "conversations": conversations,
        "active_conversation": active_conversation,
    })


@login_required
def conversation_view(request, convo_id):
    convo = get_object_or_404(Conversation, id=convo_id)

    # permission check
    if request.user not in (convo.user1, convo.user2):
        return redirect("inbox_pro")

    if request.method == "POST":
        msg = request.POST.get("message")
        if msg.strip():
            Message.objects.create(
                conversation=convo,
                sender=request.user,
                body=msg
            )

    return render(request, "JobFinder_app/inbox_pro.html", {
        "conversations": Conversation.objects.filter(
            user1=request.user
        ) | Conversation.objects.filter(
            user2=request.user
        ),
        "active_conversation": convo
    })

#def base_view(request):
    #return render(request,'/base.html')



# @login_required
# def send_interview(request, job_id, seeker_id):
#     job = get_object_or_404(Job, id=job_id)
#     seeker = get_object_or_404(User, id=seeker_id)

#     # only the job owner can send interviews
#     if job.user != request.user:
#         return redirect("employer_dashboard")

#     if not job.interview_questions:
#         # nothing to send; you might flash a message later
#         return redirect("employer_dashboard")

#     # create or reuse an assignment
#     assignment, created = InterviewAssignment.objects.get_or_create(
#         job=job,
#         employer=request.user,
#         seeker=seeker,
#         defaults={"questions": job.interview_questions},
#     )
#     if not created:
#         # keep questions in sync if changed
#         assignment.questions = job.interview_questions
#         assignment.save()

#     # send a Message into the seeker's inbox
#     Message.objects.create(
#         sender=request.user,
#         receiver=seeker,
#         subject=f"Interview for {job.title}",
#         body="You have been invited to complete a video interview for this job.",
#         job=job,
#     )

#     return redirect("employer_dashboard")

# def employerone_view(request):
#     if request.method == 'POST':
#         form = EmployerFormOne(request.POST)
#         if form.is_valid():
#             form.save(form.cleaned_data)
#             return redirect('employerviewtwo')
    
#     else:
#         form = EmployerFormOne()
#         return render(request,'JobFinder_app/employerexone.html',context={'form': form})
        

# def employertwo_view(request):
#     if request.method == 'POST':
#         form = EmployerFormTwo(request.POST)   
#         if form.is_valid():
#             form.save(form.cleaned_data)
#             return redirect('employerviewthree')
        
#     else:
#         form = EmployerFormTwo()
#         return render(request,'JobFinder_app/employerextwo.html',context={'form': form})
    

# def employerthree_view(request):
#     if request.method == 'POST':
#         form = EmployerFormThree(request.POST)
#         if form.is_valid():
#             form.save(form.cleaned_data)
#             return render(request,'JobFinder_app/thanks.html')
        
#     else:
#         form = EmployerFormThree()
#         return render(request,'JobFinder_app/employerexthree.html',context={'form': form})

# def employer_dashboard(request):
#     employer_user = request.user
#     matches = match_seekers(employer_user)

#     seekers = User.objects.filter(id__in=matches)

#     return render(request, "JobFinder_app/employer_dashboard.html", {
#         "seekers": seekers
#     })