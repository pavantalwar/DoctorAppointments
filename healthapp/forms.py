from django import forms
from .models import book_appointments, doctors
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class book_appointments_form(forms.ModelForm):
    doctor_name = forms.ModelChoiceField(
        queryset=doctors.objects.all(),
        empty_label="Select Doctor",
        to_field_name='doctorname',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = book_appointments
        fields = '__all__'

    def clean_email(self):
        em = self.cleaned_data.get("email")
        if not "@gmail.com" in em:
            raise forms.ValidationError("Please provide a valid Gmail address!")
        return em

    def clean(self):
        cleaned_data = super().clean()

        booking_date = cleaned_data.get("date")
        booking_time = cleaned_data.get("time")
        doctor_name = cleaned_data.get("doctor_name")

        if booking_date and booking_time:
            combined_datetime = datetime.datetime.combine(booking_date, booking_time)
            now = timezone.now()

            if timezone.is_aware(now) and timezone.is_naive(combined_datetime):
                combined_datetime = timezone.make_aware(combined_datetime, timezone.get_current_timezone())

            if combined_datetime < now:
                raise ValidationError("Booking date and time must be in the future!")

            #  New Validation: Allow only 10-minute interval times
            if booking_time.minute % 10 != 0:
                raise ValidationError("Appointment time must be in 10-minute intervals (e.g., 9:00, 9:10, 9:20).")

        # Validate doctor's working hours
        if doctor_name and booking_time:
            try:
                doctor = doctors.objects.get(doctorname=doctor_name)
            except doctors.DoesNotExist:
                raise ValidationError("Selected doctor does not exist!")

            if not doctor.starttime < booking_time < doctor.endtime:
                raise ValidationError(
                    f"Booking time must be between {doctor.starttime.strftime('%H:%M')} and {doctor.endtime.strftime('%H:%M')} for Dr. {doctor_name}."
                )

        # Validate slot availability
        if doctor_name and booking_date and booking_time:
            if book_appointments.objects.filter(
                doctor_name=doctor_name,
                date=booking_date,
                time=booking_time
            ).exists():
                raise ValidationError("This slot is already booked. Please choose a different time.")

        return cleaned_data
