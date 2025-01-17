from django.db import models
from accounts.models import User

# this model is to define schema for ticket and insert data into it.
class ticket_model(models.Model):
    
    Ticket_ID = models.CharField(primary_key=True,max_length=20)
    # Ticket_ID = models.UUIDField(primary_key=True,auto_created=True)
    Department_Name = models.CharField(max_length=30)
    Title = models.CharField(max_length=100)
    Description = models.JSONField()
    is_accepted = models.BooleanField(default=False)
    Created_At = models.DateTimeField(auto_now_add=True)
    Status = models.JSONField()
    is_closed = models.BooleanField(default=False)
    
    #primary key of users table as foreign key to store which ticket is raised by which user
    Raised_By = models.ForeignKey(User,on_delete=models.CASCADE)  
    Accepted_By = models.CharField(max_length=20,null=True,default='To Be Accepted')
   
    class Meta:
        db_table = 'tickets'                      #name of the db table
        verbose_name_plural = 'Queries_corner'    #name of the model to be displayed in admin panel

   # this func returns all the fields of the object of a model in string when called     
    def __str__(self):
        return '{}'.format(
            self.Ticket_ID,
            )

#this model will store the frequently raised tickets created by the HODs
class frqt_tkt_model(models.Model):
    dept_name = models.CharField(max_length=50,blank=True)
    frqt_tkt_name = models.CharField(max_length=50) 
    image = models.ImageField(upload_to='frqt_tkt_imgs/')
    fields = models.JSONField()
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'frequently_raised_tkts_table'

    def __str__(self):
        return "{},{},{},{},{}".format(
            self.dept_name,
            self.frqt_tkt_name,
            self.image,
            self.fields,
            self.is_available,
        )
    
#this model handles the messgages of various tickets with db
class comments_model(models.Model):
    response = models.TextField(max_length=300)
    created_at = models.DateTimeField()
    commented_By = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,default='none')
    for_ticket_id = models.ForeignKey(ticket_model,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Solutions_corner'   #name of the db table 
        
    def __str__(self) -> str:
        return "{},{},{}".format(
            self.response,
            self.created_at,
            self.for_ticket_id
        )
    