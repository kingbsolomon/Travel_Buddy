from django.db import models
import re
from datetime import date, datetime


class UserManager(models.Manager):
    PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
    
    def user_validator(self, postData):
        errors = {}
        user = User.objects.filter(username=postData['username'])

        if (len(postData['name'])<3): #will add alphanumeric validator later due to spaces
            errors['name'] = "Please Enter a Valid Name (Must Be At Least 3 Characters)"
        if (len(postData['username'])<3) or (not postData['username'].isalpha()):
            errors['username'] = "Please Enter a Valid Username (Must Be At Least 3 Characters)"
        if user:
            if user[0].username == postData['username']:
                errors['username'] = "Username Used on Previous Registration. Please Login."
        if not self.PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must be Minimum eight characters, at least one uppercase letter, one lowercase letter, one number, and one special character"
        if not postData['confirm_password'] == postData['password']:
            errors['confirm_password'] = "Passwords Must Match"
        return errors

    def login_validator(self, postData):
        errors_login = {}
        if (len(postData['username'])<3) or (not postData['username'].isalpha()):
            errors_login['username'] = "Please Enter a Valid Username (Must Be At Least 3 Characters)"
        if not self.PASSWORD_REGEX.match(postData['password']):
            errors_login['password'] = "Password must be Minimum eight characters, at least one uppercase letter, one lowercase letter, one number, and one special character"
        return errors_login

class TripManager(models.Manager):

    def trip_validator(self, postData):
        errors = {}
        DATE_REGEX = re.compile(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')

        if (len(postData['destination'])<1):
            errors['destination'] = "Please Enter a Valid Destination"
        if (len(postData['desc'])<3):
            errors['desc'] = "Please Enter a Valid Description"
        if not DATE_REGEX.match(postData['travel_start']):
            errors["travel_start"] = "Invalid Start Date (yyyy-mm-dd)"
        if DATE_REGEX.match(postData['travel_start']):
            if not datetime.strptime(postData['travel_start'],"%Y-%m-%d")  > datetime.today():
                errors['travel_start'] = "Invalid Start Date. Travel Start Should be in the Future."
        if not DATE_REGEX.match(postData['travel_end']):
            errors["travel_end"] = "Invalid End Date (yyyy-mm-dd)"
        if not postData['travel_end'] > postData['travel_start']:
            errors['travel_end'] = "Invalid End Date. Travel End Date Cannot Be Before Start Date."
        return errors

# Create your models here
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    planned_by = models.ForeignKey(User, related_name="planner", on_delete = models.CASCADE)
    travel_start = models.DateField()
    travel_end = models.DateField()
    desc = models.TextField()
    users_joining = models.ManyToManyField(User, related_name="trips")
    objects = TripManager()
    
