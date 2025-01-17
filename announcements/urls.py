from .views import *
from django.urls import path
from .views import * 

urlpatterns = [  

    path('announcements/form',new_announcement_form,name="new_announcement"),   # gets the announcement form to make one on request.

    path('announcements/new',create_announcement,name="broadcast"),         # stores the new announcement made by a dept into db on submittion.
    
    path('manage/announcements/',manage_dept_annoucements,name='manage_announcements'), #to make and manage various announcements made by different depts.

    path('delete-announcement/<dept>/<name>/',delete_dept_announcement,name='delete_announcement'), #to delete an announcement on click by dept members.

     path('announcements/',announcements,name="announcements"),              # to display the announcements made by different depts.
]