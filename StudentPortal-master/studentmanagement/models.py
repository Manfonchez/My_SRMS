from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CERT_STATUS = (
    ('Collected', 'Collected'),
    ('Not collected', 'Not collected')
)

FEE_STATUS = (
    ('Ongoing', 'Ongoing'),
    ('Completed', 'Completed')
)

COURSE_LEVEL = (
    ('Certificate', 'Certificate'),
    ('Diploma', 'Diploma')
)

EXAM_RESULTS = (
    ('Passed', 'Passed'),
    ('Failed', 'Failed'),
    ('Referral', 'Referral')
)

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,  null=True)
    reg_number = models.CharField(max_length=20,  null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    course_name = models.CharField(max_length=100, null=True)
    course_level = models.CharField(
        max_length=200, null=True, choices=COURSE_LEVEL)
    results = models.CharField(max_length =100, null=True, choices=EXAM_RESULTS)
    fee_required = models.IntegerField(null=True)
    fee_paid = models.IntegerField(null=True)
    fee_balance = models.IntegerField(null=True)
    fee_status = models.CharField(
        max_length=200, null=True, choices=FEE_STATUS)
    cert_status = models.CharField(
        max_length=200, null=True, choices=CERT_STATUS)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.full_name)

class Contact(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.CharField(max_length=200)
