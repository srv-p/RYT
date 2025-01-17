from django.contrib import admin
from .models import *
#since we are customizing the model in admin panel we have to extend the in-built UserAdmin class of django
class tkts_sort(admin.ModelAdmin):
    model = ticket_model
    list_display = ("Ticket_ID","Title","Department_Name","Created_At","Raised_By","status_display","Accepted_By")
    list_filter = ("Department_Name","Created_At",)
    fields = ('Ticket_ID',"Title","Department_Name","Description","Created_At","Raised_By","status_display","Accepted_By")
    search_fields = ("Ticket_ID","Raised_By_id")
    ordering = ("-Created_At",)
    #to make all the fields as read-only for the tickets raised by all other users
    readonly_fields = list_display
    list_per_page = 10

    def status_display(self,obj):
        return obj.Status.get('current')
    
    status_display.short_description = 'Status'

    def raised_id(self,obj):
        return obj.raised_by.userID
    
    # to modify raised_id as raised_by in table for user display
    raised_id.short_description = 'Raised_By'
    # truncated_fields
    
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None, *args , **kwargs) -> bool:
        return False

admin.site.register(ticket_model,tkts_sort)
