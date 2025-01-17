from time import strptime
from django.http import *

from .forms.tktForm import *
from django.shortcuts import *
from django.db.models.functions import TruncSecond
from accounts.views import *
from .views import *
import datetime

# this view is called to store a frt into db when a hod submits the new frt 
@login_required(login_url='/login')
def new_frt_create(request):

    field_names={}                           #this dict will store the field names and their types as submitted by the hod in new frt creation.
    
    if request.method == "POST":
        values=list(request.POST.values())   #request.post.values() will fetch all the values entered into input tags by the user.
        values = values[2:]                  # the 1st two inputs are csrf_token and title of the frt & these are handled differently.

        # Now , values is a list where even element is name of field and odd element is its type.
        # Adding them in key:value pairs in field_names to store into db
        for i in range(len(values)-1):     
                if i%2 == 0:
                    field_names[values[i]]=values[i+1]

    # print(field_names)
    if request.FILES.get('image'):                      #request.FILES.get will get the files uploaded by the user in the form.
        image = request.FILES.get('image')                                                     
    
    
    else:                                              #if user doesn't upload any image , set their dept image as bg
        image = 'media/dept-pics/{{request.user.dept_name}}'
    
    if frqt_tkt_model.objects.filter( Q(dept_name=request.user.dept_name) & Q(frqt_tkt_name = request.POST.get('tkt_name'))):
        return frt_page(request,'Ticket already exists')
    
    else:
        frqt_tkt_model.objects.create(
            dept_name = request.user.dept_name,             
            frqt_tkt_name = request.POST.get('tkt_name'),
            image = image,                                 
            fields = field_names,
            is_available = True                             #by default the frt is made available & can be changed by the hod after creating.
        )

    return redirect('/frt/')

# this view gets parameter ack from old_frts of frt_page to handle the frts of the user's dept.
def update_frt(request,tkt,ack):

    # print(tkt,ack)
    get_tkt = frqt_tkt_model.objects.get(Q(dept_name=request.user.dept_name) & Q(frqt_tkt_name=tkt))

    if ack == 'availability':                       #if user wants to change the availability of their frt.

        if get_tkt.is_available:                    #if it is already available , make it unavailable
            get_tkt.is_available = False

        else:
            get_tkt.is_available = True

        get_tkt.save(update_fields=['is_available'])
    
    elif ack == 'delete':                           #if he wants to remove it , then delete it
        get_tkt.delete()

    return redirect('/frt/')

#to handle edits/delete of user raised tickets if it is not yet accepted.
def before_accept_handler(request):

    submitted_form = request.POST.copy()                            #a copy of the submitted form , since it is immutable
    submitted_form.pop('Ticket_ID')
    submitted_form.pop('csrfmiddlewaretoken')
    submitted_form.pop('Department Name')
    submitted_form.pop('Title')

    msg = ''

    if 'save' in request.POST:                                      #if user has edited the values , and clicked save
        updated_tkt = {}
        submitted_form.pop('save')
        for field,value in submitted_form.items():
            # print(field,value)
            updated_tkt[field] = value                              #add all the new values into a new dict
        updated_tkt['modified_at'] = str(datetime.datetime.now())   #to add the time when the modification is done.
        # print(updated_tkt)
        get_tkt = ticket_model.objects.get(Ticket_ID=request.POST.get('Ticket_ID'))

        old_tkt = get_tkt.Description                               #since the description is a json field , it cannot be directly updated 
        old_tkt.update(updated_tkt)                                 #store the actual values in a variable called old_tkt
        get_tkt.save()  
        msg = 'Successfully updated the ticket with ID ' +  request.POST.get('Ticket_ID')  #change the dict with updated values and save into db
        # print(get_tkt)


    else:
        # print('deleting this ticket')                             #if user wants to delete the ticket , remove from db                       
        get_tkt = ticket_model.objects.get(Ticket_ID=request.POST.get('Ticket_ID'))
        get_tkt.delete()
        msg = 'Successfully deleted the ticket with ID ' + request.POST.get('Ticket_ID')

    return fetch_user_tkts(request,'raised_tkts',msg)

#to help raise_tkt view to create a ticket
def generate_new_tkt(user,dept,tkt_name,descp):

    #to pre-fill certain fields like date,id,created_time and accepted_status when user submits a ticket
    default = pre_values(dept)

    #as long as a ticket with generated tkt_id exists , generate new tkt_id
    while ticket_model.objects.filter(Ticket_ID = default['tkt_id']):
        default = pre_values(dept)

    #inserting a new ticket into tickets table
    new_tkt = ticket_model.objects.create(
            Ticket_ID = default['tkt_id'],
            Title = tkt_name,
            Description = descp,
            Department_Name = dept,
            Status = {
                        'current': default['accept_status'],
                        'colour': 'Green',
                    },
            Raised_By_id = user
        )

    return new_tkt
    
#this view is called when a user wants to raise a ticket
@login_required(login_url='/login')
def raise_tkt(request):
    if request.method == 'POST':
            dept_name = request.POST.get('dept_name')
            tkt_name = request.POST.get('tkt_name')

            fields = request.POST.dict()
            fields.pop('csrfmiddlewaretoken')
            fields.pop('dept_name')
            fields.pop('tkt_name')

            new_tkt = generate_new_tkt(request.user,dept_name,tkt_name,fields)      #pass above fields to generate_tkt view to insert a ticket into db

            if new_tkt:                                                             #to display ack message to the user on raising a ticket
                message = 'Your ticket has been raised with ID '+ new_tkt.Ticket_ID +'. '
                message = message + new_tkt.Department_Name + ''' department typically responds between 4pm to 6pm on all working days. Your ticket is editable as long as its not accepted.'''
                return fetch_user_tkts(request,'user_tkts',message)                 #if success , reidrect to home page.
           
            else:
                # print('error occured')
                return HttpResponse('not success')
    else:
        # print('error occured')  
        return redirect('/')  

#to update the status of the ticket if its acceptance/reply is delayed
@login_required(login_url='/login')
def update_status(request,status,*args):

    if not args:                                                #if it is accepted , change its status to in-progress
        status['current'] = 'In Progress'
        status['colour'] = 'success'
        status['last_commented_by'] = str(request.user)
        status['commented_at'] = str(datetime.datetime.now())

    elif isinstance(args[0],comments_model):                    #if there is a new reply , after a long period of time , changes its status from Pending to in-progress
        status['current'] = 'In Progress'
        status['last_commented_by'] = str(request.user)
        status['commented_at'] = str(datetime.datetime.now())
        status['colour'] = 'success'

    elif status == '':                                          #only executed when called by fetch_user_tkts
        for each_tkt in args[0]:
            Status = each_tkt['Status']
            current_time = datetime.datetime.now()
            if 'commented_at' in Status:
                date_format = '%Y-%m-%d %H:%M:%S.%f'
                last_commented_time = datetime.datetime.strptime(Status['commented_at'],date_format)
                time_difference =  current_time - last_commented_time 
              # time_difference = (time_difference.total_seconds())/3600.0

            #if the reply is delayed , change the status of the ticket from in-progress to Pending.
                if time_difference.total_seconds() > 10 and Status['last_commented_by'] != each_tkt['Accepted_By']:
                    Status['colour'] = 'warning'
                    get_tkt = ticket_model.objects.get(Ticket_ID=each_tkt['Ticket_ID'])
                    get_tkt.Status['colour'] = 'warning'
                    get_tkt.Status['current'] = 'Pending'
                    get_tkt.save(update_fields=['Status'])

    return status

#this view handles the response of a user to a ticket on submission. Takes the tkt id as parameter
@login_required(login_url='/login')
def response_handler(request,tkt_id):
           
    incoming_user = str(request.user)                                       #gets the reg.no of the user who is accessing above ticket
    reply = request.POST.get('reply')                                       #gets the reply/comment made by the user.
                                    
    get_tkt = ticket_model.objects.get(Ticket_ID=tkt_id)

    raised_by = str(get_tkt.Raised_By)                                      #converts data field from database into string
    accepted_by = str(get_tkt.Accepted_By)

    if not get_tkt.is_accepted:                                             #checks if the ticket is not accepted by anyone.                                        
            get_tkt.Accepted_By = incoming_user                             #updates the necessary fields of the ticket into database.
            get_tkt.is_accepted = 'True'  
            update_status(request,get_tkt.Status)
            get_tkt.save(update_fields=['is_accepted','Status','Accepted_By'])
            add_comment(request,get_tkt,reply)
            return redirect('/get_tkts/dept_tkts')

    if get_tkt.is_accepted:                                                 #checks if the ticket is already accepted.
       
        if incoming_user != raised_by and incoming_user != accepted_by and not request.user.is_hod:     #checks if the user is neither the raised or nor the accepted one.
            warning = 'You cannot reply to a ticket unaccepted by you.'     #prevents the user to reply for the above ticket if the above condition is true.
            
            if incoming_user == raised_by:
                return fetch_user_tkts(request,'user_tkts',warning)
           
            else:
                return fetch_user_tkts(request,'dept_tkts',warning)
        
        else:
            comment = add_comment(request,get_tkt,reply)                              #if the replying user is either of them , let him reply and add it into database.
            update_status(request,get_tkt.Status,comment)
            get_tkt.save(update_fields=['Status'])

            if incoming_user == raised_by:                                  #if it is the raised one , redirect him to raised_tkts page
                return redirect('/get_tkts/raised_tkts')
            
            else:                                                           #if he is depatment member , redirect him to his dept_page
                return redirect('/get_tkts/dept_tkts')
            
#to insert the user's reply/comment for a ticket into db
def add_comment(request,fetch_tkt,reply):
    new_comment = comments_model.objects.create(
        response = reply,
        created_at = datetime.datetime.now(),
        for_ticket_id = fetch_tkt,
        commented_By = request.user
    )
    return new_comment

#to allow user to close a ticket raised by them on completion.
@login_required(login_url='/login')
def close_handler(request,tkt_id):      
         get_tkt = ticket_model.objects.get(Ticket_ID=tkt_id)
         get_tkt.Status['current'] = 'Completed'
         get_tkt.Status['colour'] = 'success'
         get_tkt.is_closed = True
         get_tkt.save(update_fields=['Status','is_closed'])
         msg = 'Ticket with ID ' + tkt_id + ' has been successfully closed. You can no longer converse in it.'
         return fetch_user_tkts(request,'raised_tkts',msg)

# to fetch the dept tkts of the user or tickets raised by him on request
@login_required(login_url='/login')
def fetch_user_tkts(request,for_his_dept,*args):

    message = ''

    if args:                                            #to display the ack message to the user on successfully raising a ticket
         message = args[0]

    user = str(request.user)

    if not request.user.is_authenticated:               #redirect user to login page if he is not authenticated
        return render_login_page(request)
    
    if request.session['user_type'] == 'dept' and for_his_dept != 'dept_tkts':
        raise Http404('Page Not found')
    
    elif request.session['user_type'] != 'dept' and for_his_dept == 'dept_tkts':
        raise Http404('Page Not found')     

    if for_his_dept == 'dept_tkts':              #if user asks for his dept tkts , fetch them. TruncSecond method truncates the time value to seconds.
        user_tkts = ticket_model.objects.filter( 
            Department_Name=request.user.dept_name
            ).annotate(Created_at=TruncSecond('Created_At')
                     ).only('Ticket_ID','Title','Created_At','Raised_By_id','Status','Accepted_By'
                             ).values('Ticket_ID','Title','Created_at','Raised_By_id','Status','Accepted_By').order_by('-Status__current','-Created_At')
        for_his_dept = True
    
    else:                                             #else fetch tickets raised by him and order them by latest.  
       user_tkts = ticket_model.objects.filter(
         Raised_By_id=request.user
           
           ).annotate(Created_at=TruncSecond('Created_At')
                      ).only('Ticket_ID','Title','Department_Name','Created_At','Status','Accepted_By'
                             ).values('Ticket_ID','Title','Department_Name','Created_at','Status','Accepted_By').order_by('-Status__current','-Created_At')
       for_his_dept = False

    update_status(request,'',user_tkts)         #to update the status of the tickets if the acceptance/reply is delayed

    fields = []                                 #fields to be displayed in the table for the user
    if user_tkts:
        for key in dict(user_tkts[0]):
            fields.append(key)
        
    fields.insert(0,'S.No')
 
    fields = [field.replace('_',' ') for field in fields]   #to remove _ in the fields

    for each_tkt in user_tkts:
        if each_tkt['Status']['current'] == 'To Be Accepted':           #if the ticket status is still to be accepted and is delayed
            current_time = datetime.datetime.now()                      #convert it into red and to make it blink in ui.
            current_time = current_time.replace(microsecond=0)
            created_time = each_tkt['Created_at']
            time_diff = current_time - created_time
            time_diff = time_diff.total_seconds()
            if time_diff > 60:
                each_tkt['Status']['commented_at'] = time_diff
                each_tkt['Status']['colour'] = 'danger'
        # print(each_tkt)

    #html table that will render the tickets of the user/dept in ui
    tkts_table = Template("""
        <div style="margin-bottom:10%;margin-left:5%;margin-right:5%;margin-top:5%;"><center><h1 class="text-secondary" style="margin:3%;font-family:Bellota Text;">
        {% if for_his_dept %}
        {{dept_name}} Department Tickets 
        {% else %}
        {{user}} Raised Tickets 
        {% endif %}
        </h1></center>                                      
        <table class="table table-hover table-bordered" id="user_tkts">

            <thead>
            <tr>
                {% for each_field in fields %}
                <th>{{each_field}}</th>
                {% endfor %}
            </tr>
            </thead>

            <tbody class="text-center" id='tkts_body'>
                {% for tkt in user_tkts %}
                    {% if tkt.Raised_By_id != user %}
                    <tr id="reply_for_{{tkt.Ticket_ID}}" data_parent_value="{{tkt.Ticket_ID}}" >

                <td>{{forloop.counter}}
                {% if tkt.Status.current == 'In Progress' and tkt.Status.last_commented_by != user or tkt.Status.current == 'Pending' and tkt.Status.last_commented_by != user %}
                {% if not for_his_dept or tkt.Accepted_By == user %}
                <i class="fa-sharp fa-solid fa-circle-dot fa-beat-fade" style="color: #05ff09;"></i>
                {% endif %}
                {% endif %}
                </td>  
                    {% for key,value in tkt.items %}
                    {% if key == 'Accepted_By' %}
                        {% if value == 'To Be Accepted' %}
                        <td><img src="/static/admin/img/icon-no.svg" alt="False"></td>
                        {% else %}
                        <td>
                        {{value}}
                        </td>
                        {% endif %}
                    {% elif key == 'Status' %}
                    <td>
                        <span
                            class = 'text-{{tkt.Status.colour}}'
                        >{{value.current}}</span>
                    </td>
                    {% else %}
                    <td>{{value|safe}}</td>
                    {% endif %}
                    {% endfor %}
                    {% endif %}
                {% endfor %}
            </tbody>
            </table>
            </div>

            {% if message != '' %}
            <script>
                window.alert("{{message}}")
                window.location.href = "/get_tkts/raised_tkts";
            </script>
            {% endif %}
    """)
   
    tkts_table = tkts_table.render(Context({
        'fields':fields,
        'user_tkts':user_tkts,
        'message':message,
        'user':user,
        'dept_name':request.user.dept_name,
        'for_his_dept':for_his_dept
        }))

    return render(request,'base.html',{'view_html':tkts_table})

