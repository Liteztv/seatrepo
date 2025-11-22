from django.shortcuts import render


#def base_view(request):
    #return render(request,'/base.html')

def home_view(request):
    return render(request,'JobFinder_app/home.html')
