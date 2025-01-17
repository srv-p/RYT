from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


#a custom user model which extends Abstract Base User , the in-built user model in django to define custom fields as desired by user.
class User(AbstractBaseUser,PermissionsMixin):
    
    dept_choices = (
        ('Stores','Stores'),
        ('Kitchen','Kitchen'),
        ('Holistic Health','Holistic Health'),
        ('Aura','Aura'),
        ('Maintenance','Maintenance'),
        ('Altar','Altar'),
        ('Ankur','Ankur'),
        ('Hostel Essentials','Hostel Essentials'),
        ('Multimedia','Multimedia'),
        ('Music','Music'),
        ('Telephone','Telephone'),
        ('Sai Replica','Sai Replica'),
        ('Sports','Sports'),
        ('InSaight','InSaight'),
        ('Cardroom','Cardroom')
    )

    student_choices = (
        ('I UG BBA','I UG BBA'),
        ('I UG BSc','I UG BSc'),
        ('II UG BBA','II UG BBA'),
        ('II UG BSc','II UG BSc'),
        ('III UG BBA','III UG BBA'),
        ('III UG BSc','III UG BSc'),
        ('I PG MSc','I PG MSc'),
        ('II PG MSc','II PG MSc'),
        
    )

    userID = models.CharField(max_length=6,primary_key=True,unique=True,default='000000')
    name = models.CharField(max_length=20,default='Enter user name here')
    dept_name = models.CharField(max_length=20,choices=dept_choices)
    student_year = models.CharField(max_length=10,choices=student_choices,blank=True)
    can_accept_tickets = models.BooleanField(default=False)
    can_modify_frts = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "userID"                               #setting userID as primary key 
    REQUIRED_FIELDS = ["name",]                 #these fields are mandatory to create a user object.
    
    class Meta:
        db_table = 'Users'                                  #name of the table to be as in db

    objects = CustomUserManager()                          #Custom User Manager class creates a new user.

    def __str__(self):                                      #returns the userID of a user when called
        return '{}'.format(
            self.userID,
            )
    
    def check_password(self, raw_password: str) -> bool:    #checks if the entered password matches with the hashed password.
        return super().check_password(raw_password)
    
#Models for event hosting
class Student(models.Model):
    name=models.CharField(max_length=20)
    roll=models.IntegerField(default=000000)

    #event= models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

