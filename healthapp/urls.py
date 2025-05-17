from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("signup/",views.signup_page, name="signup_page"),
    path("home/", views.home_page, name="home_page"),
    path("signinhelp/", views.signinhelp_page, name="signinhelp_page"),
    path("doctors/",views.doctors_page, name="doctors_page"),
    path("bookappointment/",views.book_appointment_view, name="book_appointment_page"),
    path('appointment/success/<int:appointment_id>/', views.appointment_success_view, name='appointment_success'),
    path("allappointments/", views.all_appointments, name="all_appointments"),
    path("doctorappointments/", views.doctor_appointments, name="doctor_appointments"),
    path("allapp2/",views.all_appointments2, name="all_appointments2")

]