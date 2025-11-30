from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import SeekerFormOne, SeekerFormTwo, SeekerFormThree, EmployerFormOne, EmployerFormTwo, EmployerFormThree, RegistrationForm, LoginForm
# from django.urls import reverse
from .models import SeekerModelOne, SeekerModelThree, SeekerModelTwo, EmployerModelOne, EmployerModelThree, EmployerModelTwo, Profile


def match_seekers(employer_user):
    """ Returns seekers where ALL 3 seeker models meet or exceed employer requirements """
    
    emp1 = EmployerModelOne.objects.get(user=employer_user)
    emp2 = EmployerModelTwo.objects.get(user=employer_user)
    emp3 = EmployerModelThree.objects.get(user=employer_user)

    seekers1 = SeekerModelOne.objects.all()
    seekers2 = SeekerModelTwo.objects.all()
    seekers3 = SeekerModelThree.objects.all()

    # FILTER FOR MODEL ONE (only employer fields > 0)
    filters_1 = {
        f"{field}__gte": getattr(emp1, field)
        for field in ["total_years_of_experience", "html_experience", "css_experience"]
        if getattr(emp1, field) and getattr(emp1, field) > 0
    }
    seekers1 = seekers1.filter(**filters_1)

    # MODEL TWO
    fields2 = ["python_experience", "java_experience", "javascript_experience",
               "cplusplus_experience", "csharp_experience", "ruby_experience"]
    filters_2 = {
        f"{field}__gte": getattr(emp2, field)
        for field in fields2
        if getattr(emp2, field) and getattr(emp2, field) > 0
    }
    seekers2 = seekers2.filter(**filters_2)

    # MODEL THREE
    fields3 = [f.name for f in EmployerModelThree._meta.fields if f.name not in ("id", "user")]
    filters_3 = {
        f"{field}__gte": getattr(emp3, field)
        for field in fields3
        if getattr(emp3, field) and getattr(emp3, field) > 0
    }
    seekers3 = seekers3.filter(**filters_3)

    # MATCH SEEKERS WITH ALL 3 MODELS
    seeker_users = set(seekers1.values_list("user", flat=True)) \
                & set(seekers2.values_list("user", flat=True)) \
                & set(seekers3.values_list("user", flat=True))

    return seeker_users


def employer_dashboard(request):
    employer_user = request.user
    matches = match_seekers(employer_user)

    seekers = User.objects.filter(id__in=matches)

    return render(request, "JobFinder_app/employer_dashboard.html", {
        "seekers": seekers
    })

def seeker_dashboard(request):
    return render(request, "JobFinder_app/eeker_dashboard.html")



#def base_view(request):
    #return render(request,'/base.html')

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
    
def employerone_view(request):
    if request.method == 'POST':
        form = EmployerFormOne(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)
            return redirect('employerviewtwo')
    
    else:
        form = EmployerFormOne()
        return render(request,'JobFinder_app/employerexone.html',context={'form': form})
        

def employertwo_view(request):
    if request.method == 'POST':
        form = EmployerFormTwo(request.POST)   
        if form.is_valid():
            form.save(form.cleaned_data)
            return redirect('employerviewthree')
        
    else:
        form = EmployerFormTwo()
        return render(request,'JobFinder_app/employerextwo.html',context={'form': form})
    

def employerthree_view(request):
    if request.method == 'POST':
        form = EmployerFormThree(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)
            return render(request,'JobFinder_app/thanks.html')
        
    else:
        form = EmployerFormThree()
        return render(request,'JobFinder_app/employerexthree.html',context={'form': form})
        




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

    return render(request, "registration.html", {"form": form})


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

def employer_form_one(request):
    form = EmployerFormOne(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("employer_form2")
    return render(request, "JobFinder_app/employer_form1.html", {"form": form})


def employer_form_two(request):
    form = EmployerFormTwo(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("employer_form3")
    return render(request, "JobFinder_app/employer_form2.html", {"form": form})


def employer_form_three(request):
    form = EmployerFormThree(request.POST or None)
    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("employer_dashboard")
    return render(request, "JobFinder_app/employer_form3.html", {"form": form})

def landing_view(request):
    return render(request, "JobFinder_app/landing.html")



    
#def report_create_experience(request):
#    if request.method == 'POST':
#        form = ExperienceModel(request.POST)
#        if form.is_valid():
##            form.instance.user = request.user
