from django.db import models

# Create your models here.


class patients(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class doctors(models.Model):
    doctorname = models.CharField(max_length=20)
    starttime = models.TimeField()
    endtime = models.TimeField()

    def __str__(self):
        return self.doctorname
    

class book_appointments(models.Model):
    patient_name = models.CharField(max_length=20)
    doctor_name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField()
    description = models.CharField(max_length=250)


    def __str__(self):
        return self.patient_name;



