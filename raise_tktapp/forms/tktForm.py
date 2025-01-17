from django import forms
from django.forms import TextInput, Textarea
import random,datetime
from django.contrib.admin.widgets import *
from ..models import *
import random

#called by generate_tkt in views.py to pre-fill certain fields with default values when user raises a ticket.
def pre_values(dept_name):
        
    dept_ids = (
        ('Stores','ST'),
        ('Kitchen','KT'),
        ('Holistic Health','H2'),
        ('Aura','AU'),
        ('Maintenance','MT'),
        ('Altar','AL'),
        ('Ankur','AK'),
        ('Hostel Essentials','HE'),
        ('Multimedia','MM'),
        ('Music','MU'),
        ('Telephone','TL'),
        ('Sai Replica','SR'),
        ('Sports','SP'),
        ('InSaight','IN'),
        ('Cardroom','CR')
    )

    tkt_id = ''
    for dept in dept_ids:
        if dept[0] == dept_name:
            this_year = str(datetime.datetime.now().year)
            this_year = this_year[:1] + 'k' + this_year[2:] + '-'
            tkt_id = dept[1] + this_year + str(random.randint(00000,99999))

    accept_status = 'To Be Accepted'                       #by default pre-set accepted_status to false
    default = {                                 #pass all these values in a dictionary to generate_tkt to create a ticket
        'tkt_id': tkt_id,
        'accept_status':accept_status,
    }
    return default

#create a form for frequently raised tickets for various departments.     
class frequent_ticket_form(forms.Form):

    #over-riding __init__ of Form class to customize input fields dynamically
    #this func accepts custom input fields as parameters from views and creates a form based on the fields.

    def __init__(self,fields,*args,**kwargs):   
        super().__init__(*args,**kwargs)            #calling the parent __init__ method to create a form for below fields.
        
        for field_name,type in fields.items():                   #iterate thru a list of dictonaries to create input field for each one of them.     
            if type == 'textarea':
                 self.fields[field_name] = forms.CharField(label=field_name,widget=forms.Textarea(attrs={'class':'form-control'}))

            elif type == 'DateField':
                 self.fields[field_name] = forms.DateField(widget=AdminDateWidget(attrs=({'type':'date','min':datetime.date.today().strftime('%Y-%m-%d'),'class':'form-control'})))

            elif type == 'phone_num':
                self.fields[field_name] = forms.CharField(label=field_name,widget=forms.TextInput(attrs={'type':'tel','minlength':'7','maxlength':'15','class':'form-control','pattern':'^\d{0,15}$','placeholder':'9999-xxx-xxx'}))

            elif type == 'number':
                self.fields[field_name] = forms.CharField(widget=TextInput(attrs={'type':'number','class':'form-control'}))

            else:
                self.fields[field_name] = forms.CharField(widget=TextInput(attrs={'class':'form-control'}))

class edit_tkt(forms.Form):

    def __init__(self,tkt,field_types,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['Ticket_ID'] = forms.CharField(widget=TextInput(attrs={'class':'form-control','value':tkt['Ticket_ID'],'readonly':'readonly'}))
        self.fields['Department Name'] = forms.CharField(widget=TextInput(attrs={'class':'form-control','value':tkt['Department_Name'],'readonly':'readonly'}))
        self.fields['Title'] = forms.CharField(widget=TextInput(attrs={'class':'form-control','value':tkt['Title'],'readonly':'readonly'}))

        for key,value in tkt['Description'].items():
          if key != 'modified_at':
            if field_types[key] == 'textarea':
                self.fields[key] = forms.CharField(initial=value,widget=Textarea(attrs={'class':'form-control'}))

            elif field_types[key] == 'DateField':
                self.fields[key] = forms.DateField(widget=AdminDateWidget(attrs=({'type':'date','min':datetime.date.today().strftime('%Y-%m-%d'),'class':'form-control','value':value})))

            elif field_types[key] == 'phone_num':
                self.fields[key] = forms.CharField(widget=forms.TextInput(attrs={'type':'tel','pattern':'^\d{0,15}$','minlength':'7','maxlength':'15','class':'form-control','value':value}))
            
            elif field_types[key] == 'number':
                self.fields[key] = forms.CharField(initial=value,widget=Textarea(attrs={'type':'number','class':'form-control'}))

            else:
                 self.fields[key] = forms.CharField(widget=TextInput(attrs={'class':'form-control','value':value}))

