from django.shortcuts import render
from . forms import SeekerForm
#from . models import ExperienceModel



#def base_view(request):
    #return render(request,'/base.html')

def home_view(request):
    return render(request,'JobFinder_app/home.html')

def seeker_view(request):
    if request.method == 'POST':
        form = SeekerForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

    else:
        form = SeekerForm()
        return render(request,'JobFinder_app/seekerex.html',context={'form': form})
    
#def report_create_experience(request):
#    if request.method == 'POST':
#        form = ExperienceModel(request.POST)
#        if form.is_valid():
##            form.instance.user = request.user
