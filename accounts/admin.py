from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

#to register user model in admin panel in place of default user model.
# This class also extends in-built UserAdmin class of django since we have extended Abstract Base User to customize our user model.
class CustomUserAdmin(UserAdmin):

    #calling all the forms created in forms.py to allow admin to manage users.
    add_form = UserCreationForm     
    update_form = UserChangeForm
    model = User

    #this will make the fields as only read-only.

    #setting which fields to be displayed in the users table in admin panel
    list_display = ("userID","name","dept_name","student_year", "is_hod", 'can_accept_tickets','can_modify_frts',"is_superuser",)

    #setting various filter options for admin to fetch various users as required
    list_filter = ("dept_name","student_year",'can_accept_tickets','can_modify_frts', "is_superuser", )

    #setting pagination to show only max 10 user objects in a table.
    list_per_page = 10

    # readonly_fields = ['userID']
    #fields to be displayed in user change form
    fieldsets =  (
        ('Update user details', {'fields': ("student_year",'password','dept_name','is_hod','is_active','can_accept_tickets','can_modify_frts','is_superuser')}),
    )

    #fields to be displayed in user creation form
    add_fieldsets =  (
        ('Add new user', {'fields': ('userID','name',"student_year",'password1','password2','dept_name','is_hod','can_accept_tickets','is_active','can_modify_frts','is_superuser')}),
    )

    #allowing search of users with their userIDs
    search_fields = ("userID",)

    #the user objects in the table are ordered by their department names
    ordering = ("dept_name",)

admin.site.register(User,CustomUserAdmin)

#unregistering the default groups model of django since we don't need them.
admin.site.unregister(Group)
