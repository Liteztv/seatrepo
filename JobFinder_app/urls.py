from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view),
    path('seekerview', views.seeker_view),
    path('employerview',views.employer_view),
    path('seekerviewtwo', views.seekertwo_view, name='seekerviewtwo'),
    path('seekerviewthree', views.seekerthree_view, name='seekerviewthree')
]