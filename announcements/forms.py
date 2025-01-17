from django import forms
from django.forms import TextInput, Textarea
import datetime
from django.contrib.admin.widgets import *
from .models import *
from django.forms import ModelForm

class Announcement_Form(ModelForm):
    class Meta:
        model = announcements_model
        fields = ['Title','Announcement','Validity']

        widgets = {

            'Title' : TextInput(attrs={'class': 'form-control','placeholder':'Breif Name of Announcement'}),   #class form-control is bootstrap's class to add styling to input fields
            'Announcement' : Textarea(attrs={'class': 'form-control','placeholder':'Enter the Announcement Here !!'}),
            'Validity' : forms.DateTimeInput(attrs={'type':'datetime-local','min':datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),'class': 'form-control'}),
        }
