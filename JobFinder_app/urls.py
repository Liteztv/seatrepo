from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_view),
    path('seeker', views.seeker_view)
]