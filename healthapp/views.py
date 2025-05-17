from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import patients, book_appointments, doctors
from django.core.mail import send_mail
from django.conf import settings
from .forms import book_appointments_form
from django.shortcuts import get_object_or_404


# Create your views here.


def home_page(request):
    return render(request, 'home.html')

def signup_page(request):
    if request.method == "POST":
        username = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']

        record = patients.objects.filter(email=email)
        if not record.exists():
            data = patients(username=username, email=email, password=password)
            data.save()
            return redirect('login_page')
        else:
            return render(request, 'signup_page.html', {
                "data": f"User already exists with this email: {email}"
            })

    return render(request, 'signup_page.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        data = patients.objects.filter(username = username, password = password)
        if data.exists():
            return redirect ('home_page')
        else:
            return render(request,'login_page.html',{"data":"incorrect username or password"})

    return render(request, 'login_page.html')



def signinhelp_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        data = patients.objects.filter(email=email).first()  # get first match directly

        if data:
            subject = "Your Login Credentials"
            message = f"""
Hi {data.username},

As requested, here are your login credentials:

Username: {data.username}
Password: {data.password}   # ⚠️ Not recommended to send passwords via email

Please keep this information confidential.

Regards,
Vcude Hospitals Support Team
"""
            send_mail(
                subject,
                message,
                None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                [email],
                fail_silently=False,
            )

            return render(request, 'signinhelp_page.html', {
                "data1": "Your login credentials have been sent to your email."
            })

        else:
            return render(request, 'signinhelp_page.html', {
                "data2": "You are not signed up yet. Please sign up first."
            })

    return render(request, 'signinhelp_page.html')



def doctors_page(request):
    return render(request, 'doctors_page.html')









def book_appointment_view(request):
    if request.method == "POST":
        form = book_appointments_form(request.POST)
        if form.is_valid():
            appointment = form.save()

            # Send confirmation email to patient
            subject = "Appointment Confirmation - Vcube Hospitals"
            message = f"""
            Dear {appointment.patient_name},

        Your appointment has been successfully booked!

            Appointment Details:
            Doctor: Dr. {appointment.doctor_name}
            Date: {appointment.date}
            Time: {appointment.time}

            Thank you for choosing Vcube Hospitals.
            We look forward to serving you!

            Best regards,
            Vcube Hospitals Team
            """
            recipient_list = [appointment.email]

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )

            # Redirect to success page with appointment ID
            return redirect('appointment_success', appointment_id=appointment.id)
    else:
        form = book_appointments_form()

    return render(request, 'bookappointment.html', {'form': form})







def appointment_success_view(request, appointment_id):
    appointment = get_object_or_404(book_appointments, id=appointment_id)
    return render(request, 'appointment_success.html', {'appointment': appointment})




def all_appointments(request):
    appointments = book_appointments.objects.all()
    return render(request, 'all_appointments.html',{"appointments":appointments})



def doctor_appointments(request):
    if request.method == "POST":
        doctor = request.POST['doctor']
        date = request.POST['date']
        app = book_appointments.objects.filter(doctor_name = doctor, date=date)
        if app.exists():
            return render(request,'doctor_appointments.html',{"appointments":app})
        else:
            return render(request,'doctor_appointments.html',{"appointments":[]})
    doctorsdata = doctors.objects.all()
    return render(request, 'doctor_appointments.html',{"data":doctorsdata})



from django.shortcuts import render
from .models import book_appointments
from django.db.models import Q

def all_appointments2(request):
    query = request.GET.get('q', '').strip()
    appointments = book_appointments.objects.all()

    if query:
        appointments = appointments.filter(
            Q(doctor_name__icontains=query) |
            Q(date__icontains=query)  # assuming date field is stored in 'YYYY-MM-DD'
        )

    return render(request, 'all_appointments2.html', {"appointments": appointments})

