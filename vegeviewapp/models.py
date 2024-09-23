from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    Country = CountryField(blank=False)
    phone_number = PhoneNumberField(blank=False, null=False) 
    organization = models.CharField(max_length=150, blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)
    data_use = models.CharField(max_length=50, blank=True, null=True)
    additional_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
