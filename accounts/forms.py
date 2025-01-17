from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
# from django.forms import *
from .models import *

#to create a form for user creation. This extends in-built User Creation Form of django since we have over ridden Abstarct Base User.
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("userID","name")

#to create a form for user updation. This extends in-built User Updation Form of django since we have over ridden Abstarct Base User.
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("userID","name","can_modify_frts","can_accept_tickets")

#to create a login form for the created user model.       
class loginForm(forms.Form):
    userID = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Registration Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))

      