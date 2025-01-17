from django.db import models
from accounts.models import *

# Create your models here.
class announcements_model(models.Model):
    Title = models.CharField(max_length=30)
    Announcement = models.TextField()
    Created_At = models.DateTimeField(auto_now_add=True)
    Department_Name = models.CharField(max_length=20,default=None)
    made_by = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    Validity = models.DateTimeField()

    class Meta:
        db_table = 'Announcments'

    def __str__(self) -> str:
        return "{}.{}.{}.{}.{}.{}".format(
            self.Title,
            self.Announcement,
            self.Created_At,
            self.Department_Name,
            self.made_by,
            self.Validity
        )