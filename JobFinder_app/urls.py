from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path('seekerview', views.seeker_view),
    path('seekerviewtwo', views.seekertwo_view, name='seekerviewtwo'),
    path('seekerviewthree', views.seekerthree_view, name='seekerviewthree'),
    path('employerview',views.employer_view),
    path('employerviewone',views.employerone_view, name='employerviewone'),
    path('employerviewtwo',views.employertwo_view, name='employerviewtwo'),
    path('employerviewthree',views.employerthree_view, name='employerviewthree'),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("role-redirect/", views.role_redirect, name="role_redirect"),
    path("employer_dashboard/", views.employer_dashboard, name="employer_dashboard"),
    path("seeker_dashboard/", views.seeker_dashboard, name="seeker_dashboard"),

    # Seeker Forms
    path("seeker_form1/", views.seeker_form_one, name="seeker_form1"),
    path("seeker_form2/", views.seeker_form_two, name="seeker_form2"),
    path("seeker_form3/", views.seeker_form_three, name="seeker_form3"),

    # Employer Forms
    path("employer_form1/", views.employer_form_one, name="employer_form1"),
    path("employer_form2/", views.employer_form_two, name="employer_form2"),
    path("employer_form3/", views.employer_form_three, name="employer_form3"),
]