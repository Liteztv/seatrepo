from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view),
    path('seekerview', views.seeker_view),
    path('employerview',views.employer_view)
]