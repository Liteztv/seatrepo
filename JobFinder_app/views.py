from django.shortcuts import render,redirect
from .forms import SeekerFormOne, SeekerFormTwo, SeekerFormThree, EmployerFormOne, EmployerFormTwo, EmployerFormThree
# from django.urls import reverse
#from . models import ExperienceModel



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
    
#def report_create_experience(request):
#    if request.method == 'POST':
#        form = ExperienceModel(request.POST)
#        if form.is_valid():
##            form.instance.user = request.user
