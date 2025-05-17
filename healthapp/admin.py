from django.contrib import admin
from . models import patients, doctors, book_appointments

# Register your models here.

@admin.register(patients)
class patientsAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "password")



@admin.register(doctors)
class doctorsAdmin(admin.ModelAdmin):
    list_display = ("doctorname", "starttime", "endtime")


@admin.register(book_appointments)
class bookappointmentsAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "doctor_name", "date", "time", "email")