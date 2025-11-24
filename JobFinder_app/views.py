from django.shortcuts import render
from .forms import SeekerForm



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