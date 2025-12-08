from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path('seekerview', views.seeker_view),
    path('seekerviewtwo', views.seekertwo_view, name='seekerviewtwo'),
    path('seekerviewthree', views.seekerthree_view, name='seekerviewthree'),
    path('employerview',views.employer_view),
    path("job/<int:job_id>/edit/", views.edit_job, name="edit_job"),
    path("job/<int:job_id>/delete/", views.delete_job, name="delete_job"),
    path("inbox/", views.inbox_view, name="inbox"),
    path("job/<int:job_id>/send-interview/<int:seeker_id>/", views.send_interview, name="send_interview"),
    path("interview/<int:assignment_id>/answer/", views.answer_interview, name="answer_interview"),
    path("interview/<int:assignment_id>/review/", views.review_interview, name="review_interview"),
    path("message/<int:message_id>/", views.view_message, name="view_message"),
    path("interview/<int:assignment_id>/hire/", views.hire_from_assignment, name="hire_from_assignment"),
    path("messages/", views.inbox_pro, name="inbox_pro"),
    path("messages/<int:convo_id>/", views.conversation_view, name="conversation_view"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("role-redirect/", views.role_redirect, name="role_redirect"),
    path("employer_dashboard/", views.employer_dashboard, name="employer_dashboard"),
    path("seeker_dashboard/", views.seeker_dashboard, name="seeker_dashboard"),
    path("create_job/", views.create_job, name="create_job"),
    path("upload_resume", views.upload_resume, name="upload_resume"),
    path("resume/view/<int:user_id>/", views.view_resume, name="view_resume"),


    # Seeker Forms
    path("seeker_form1/", views.seeker_form_one, name="seeker_form1"),
    path("seeker_form2/", views.seeker_form_two, name="seeker_form2"),
    path("seeker_form3/", views.seeker_form_three, name="seeker_form3"),

    # Employer Forms
    # path("employer_form1/", views.employer_form_one, name="employer_form1"),
    # path("employer_form2/", views.employer_form_two, name="employer_form2"),
    # path("employer_form3/", views.employer_form_three, name="employer_form3"),
]