from django.contrib import admin
from .models import *

# Register your models here.
class announcements_admin(admin.ModelAdmin):
    model = announcements_model
    list_display = ('Title','Department_Name','Announcement','Created_At','made_by','Validity')
    list_filter = ('Department_Name','Created_At')
    ordering = ('-Created_At',)
    list_per_page = 10
    readonly_fields = list_display 

    def has_add_permission(self, request) -> bool:
        return False
        
    def has_change_permission(self, request, obj=None, *args , **kwargs) -> bool:
        return False

admin.site.register(announcements_model,announcements_admin)