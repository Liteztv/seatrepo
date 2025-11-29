from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view),
    path('seekerview', views.seeker_view),
    path('seekerviewtwo', views.seekertwo_view, name='seekerviewtwo'),
    path('seekerviewthree', views.seekerthree_view, name='seekerviewthree'),
    path('employerview',views.employer_view),
    path('employerviewone',views.employerone_view, name='employerviewone'),
    path('employerviewtwo',views.employertwo_view, name='employerviewtwo'),
    path('employerviewthree',views.employerthree_view, name='employerviewthree'),
]