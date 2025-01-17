from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.template import Template,Context
from django.middleware.csrf import get_token
from .forms.tktForm import *
from .models import *
from accounts.views import *  
from django.utils import timezone  

# this view is called when allowed dept members wants to handle the frts of his dept.
@login_required(login_url='/login')
def frt_page(request,*args):

    msg = ''

    if args:
         msg = args[0]
        #  print(msg)
    # variable to check if incoming user has permission to manage frts
    can_modify_frts = request.user.can_modify_frts

    exisiting_frts = frqt_tkt_model.objects.filter(dept_name=request.user.dept_name)

     # this template renders existing frts created by the depts and are available for editing/deeleting in FRT settings.
    old_frts = Template("""
    <h3 style="text-align:center;margin-top:3%;">Frequently Raised Tickets of {{dept_name}} Department
        {% if can_modify_frts %}
            <a class="text-primary" style="font-size:20px;text-decoration:none;cursor:pointer;" id="modal_opener" data-toggle="modal" data-target="#modal_html">
            <b>+ Create New Ticket</b>
            </a>
        {% endif %}
        </h3>
    <div id="container" class="container-fluid" style="margin:7%;">
            <div id="roww" class="row" style="margin-top:5%;">
            {% for each_frt in frts_list %}
                <div id="caard" class="card border-light" style="width: 19rem;">
                {% if can_modify_frts %}
                <div class="buttons" style="display:flex; justify-content:space-evenly;">
                <span><a href="{% url 'modify_frt' each_frt.frqt_tkt_name 'availability' %}">
                {% if each_frt.is_available %}
                <span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Currently available">
                <i class="fa-sharp fa-regular fa-square-check 2x"></i>
                </span>
                {% else %}
                <span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Currently unavailable">
                <i class="fa-sharp fa-regular fa-square 2x"></i>
                </span>
                {% endif %}
                </a></span>
                <span class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Delete this frt"><a href="{% url 'modify_frt' each_frt.frqt_tkt_name 'delete' %}"> 
                <i class="fa-regular fa-trash-can 2x"></i>
                </a></span> 
                </div>
                {% endif %}
                <img id="img" class="card-img-top" src="{{each_frt.image.url}}" alt="Card image cap">
                <div class="card-body">
                    <h4 class="card-title">{{each_frt.dept_name}}</h4>
                    <h3 class="card-text">{{each_frt.frqt_tkt_name}}</h4>
                    <div class="butdept"></div>
                </div>
                </div>
            {% endfor %}
            </div>
    </div>

     {% if message != '' %}
            <script>
                window.alert("{{message}}")
            </script>
            {% endif %}
    """)

    #  this is a form to create a new frt by the authorized dept members to create new frt ; available in FRT settings.
    new_frt_page = Template("""
    <form method = "post" action="create_frt" enctype = "multipart/form-data" >
            {% csrf_token %}
            <div class="input_container">
                <div id="title" class="input-group mb-3">
                    <input type="text" required class="form-control" placeholder="Title of the ticket - No special characters" name="tkt_name">
                </div>
                <div id='new_input_adder'>
                </div>
                <button type="button"  class="btn btn-warning" id="new_input" style="margin:12px;">+ Add New Field</button>
                <label for="images" class="inputfile">Upload Background Image
                    <input type="file" id="images" accept="image/*" name="image" required>
                </label>
            </div>
            <a href="{% url "create_frt" %}"><button type="submit" id="create" class="btn btn-primary" style="margin-top:10px;">Create new ticket</button></a>
    </form>
         
    """)

    # to generate a csrf_token for the above form in new_frts which is to create a new frt by hod
    csrf_token = get_token(request)   

    #  this will render the new_frt_page in template to create new frt.
    new_frt_page = new_frt_page.render(Context({'csrf_token':csrf_token}))

    #this will render the existing frts in old_frts template
    old_frts = old_frts.render(Context({'dept_name':request.user.dept_name,'frts_list':exisiting_frts,'can_modify_frts':can_modify_frts,'message' : msg}))

    # variables to be returned to the template to render
    context = {
        'view_html':old_frts,
        'modal_html':new_frt_page,
        'heading': 'New FRT Creation',
 
    }

    return render(request,'base.html',context)

#this view renders dept_names to raise tkts for it
@login_required(login_url='/login')
def tkts_departments_page(request):

    #a dictionary which will render the names of all depts ; fetches the frts of a dept on selection
      dept_list = {
            'Altar':['Your day starts & ends by US.','/media/dept_pics/altar.jpg'],

            'Ankur':['We care for the Environment around you.','/media/dept_pics/ankur.jpg'],

            'Aura':['Explore the world through books.','/media/dept_pics/aura.jpg'],

            'Cardroom & Costumes':['Talk in pictures and costumes','/media/dept_pics/cardroom.jpg'],

            'Holistic Health':['We care for your health.','/media/dept_pics/h2.jpg'],

            'Hostel Essentials':['We provide your essentials in Hostel','/media/dept_pics/he.jpg'],

            'Insaight':['Articles,Poems,content and much more','/media/dept_pics/insaight.jpg'],

            'Kitchen':['We fill your stomach with showering love of FOOD.','/media/dept_pics/kitchen.jpg'],

            'Maintenance':['100% Jugaad','/media/dept_pics/maintenance.jpg'],

            'Multimedia':['We Create your MeMories','/media/dept_pics/mm.jpg'],

            'Music':['Vibe matters','/media/dept_pics/music.jpg'],

            'Sai Replica':['Soft Copy to Hard Copy','/media/dept_pics/saireplica.jpg'],

            'Sports':['Life is a Game, play it.','/media/dept_pics/sports.jpg'],

            'Stores':['Need anything? Visit Stores! Always at your needs.','/media/dept_pics/stores.jpg'],

            'Telephone':['Never miss your connections','/media/dept_pics/telephone.jpg'],
      }
     
    # html content that consists of all the dept names as card components.
      dept_html = Template("""
        <div class="mb-5 depttext" style="font-family:Bellota Text;">
            <b>Departments</b>
        </div>

        <div id="container" class="container-fluid" style="margin:7%;">
            <div id="roww" class="row">
            {% for dept_name,desc in dept_list.items %}
                <div id="caard" class="card border-light" style="width: 19rem;">
                    <img id="img" class="card-img-top" src="{{desc.1}}" alt="Card image cap">
                    <div class="card-body">
                        <h5 class="card-title">{{dept_name}}</h5>
                        <p class="card-text">{{desc.0}}</p>
                        <div class="butdept"><a href="{% url 'frts' dept_name %}" class="btn btn-outline-danger">Frequently Raised Tickets</a></div>
                        <a href="" class="text-dark">
                    </a>
                    </div>
                </div>
            {% endfor %}
            </div>
        </div>
       """)
      
      dept_html = dept_html.render(Context({"dept_list":dept_list}))

      return render(request,'base.html',{'view_html':dept_html})

#this will get all the available frts of a dept on request by the user
@login_required(login_url='/login')
def get_dept_frts(request,check_dept):
     
     if not check_dept:
          return redirect('/')
    
     dept_frts = frqt_tkt_model.objects.filter(Q(dept_name=check_dept)& Q(is_available=True))
    #  print(dept_frts)

     #html content that will render all the frts of any dept
     frts_page = Template("""

      <div class="dept_title">
                <div class="name" style="font-family:Bellota Text;"><b>{{dept_name}}<b><br></div>
                <h3 class="frts-title"><center>Frequently Raised Tickets</center></h3> 
                <div class="scroll-text"><center>Please go through <a href="{% url 'faqs' %}">FAQs</a> of {{dept_name}} Department before raising a ticket</center></div>
      </div>

     <div id="container" class="container-fluid" style="margin:7%;">
            <div id="roww" class="row"  style="margin-top:5%;">
            {% for each_frt in dept_frts %}
                <div id="caard" class="card border-light" style="width: 19rem;">
                    <img id="img" class="card-img-top" src="{{each_frt.image.url}}" alt="Card image cap">
                    <div class="card-body" >
                        <h5 class="card-title">{{each_frt.frqt_tkt_name|escape|safe}}</h5>
                        <div class="butdept" style="margin-left:18%;"><button 
                            type="button" 
                            class="btn btn-outline-info" 
                            data-parent-value1="{{each_frt.dept_name}}" 
                            data-parent-value2="{{each_frt.frqt_tkt_name}}" 
                            id="frt_opener_{{each_frt.frqt_tkt_name}}" 
                            data-toggle="modal" 
                            data-target="#modal_html"
                            >Raise Now
                        </button></div>
                    </div>
                </div>
            {% endfor %}
            </div>
        </div>
     """)

     frts_page = frts_page.render(Context({'dept_frts':dept_frts,'dept_name':check_dept}))

     return render(request,'base.html',{'view_html':frts_page})

#to allow users to raise a new ticket
@login_required(login_url='/login')
def get_form(request,dept_name,tkt_name):

     #gets the fields of the frt
     get_frt = frqt_tkt_model.objects.get(Q(dept_name=dept_name) & Q(frqt_tkt_name=tkt_name))

     #sends the fields to the below django form ; created by the dept members during their frt creation
     create_form = frequent_ticket_form(get_frt.fields)
     create_form = create_form.as_p()
     frt_name = tkt_name
 
    #html content that will render the form in a modal
     tkt_form = Template("""
            <form method="post" action="{% url 'raise_tkt' %}" enctype = "multipart/form-data">
                {% csrf_token %}
                <input type='text' class="form-control" value="{{dept_name}}" readonly name='dept_name' id='dept_name' /><br>
                <input type='text' class="form-control" value="{{frt_name}}" readonly name='tkt_name' id='tkt_name' /><br>
                {{tkt_form}}
                <a href="{% url 'raise_tkt' %}"><button type="submit" class="btn btn-outline-success btn-lg" style="margin-top:5%;margin-left:40%;">Submit</button></a>
            </form>
     """)

     csrf_token = get_token(request)

     tkt_form = tkt_form.render(Context({'tkt_form':create_form,'csrf_token':csrf_token,'dept_name':dept_name,'frt_name':frt_name}))

     #this html content is sent to myJS on ajax request , which will append the above form in html modal
     return JsonResponse({'modal_html':tkt_form,'heading':tkt_name})

#to render the user raised tickets in editable form if not yet accepted
@login_required(login_url='/login')
def editable_ticket(request,tkt):
     dept_name = tkt['Department_Name']
     frqt_name = tkt['Title']
     field_types = frqt_tkt_model.objects.filter(Q(dept_name=dept_name) & Q(frqt_tkt_name=frqt_name)).values()
     field_types = field_types[0]['fields']

    #edit_tkt is a django form in tktForm.py which will generate an editable ticket which the fields passed to it
     tkt_html = edit_tkt(tkt,field_types)
     csrf_token = get_token(request)

    #html content that will render the ticket in editable format
     tkt_edit = Template("""
        <form method="post" action="{% url 'before_accept_handler' %}">
            {% csrf_token %}
            {{tkt_html}}
            <button type="submit" class="btn btn-success" name="save" style="margin-top:5%;">Save Changes</button>
            <button type="submit" class="btn btn-danger" name="delete" style="margin-top:5%;">Delete this Ticket</button>
        </form>
     """)

     tkt_edit = tkt_edit.render(Context({'tkt_html':tkt_html,'csrf_token':csrf_token}))
     return tkt_edit

# this will allow accepted/raised user to reply for a ticket
@login_required(login_url='/login')
def respond_form(request,tkt_id):

    get_tkt = ticket_model.objects.filter(Ticket_ID=tkt_id).values()
    get_tkt = get_tkt[0]

    # if user clicks on a ticket which is not yet accepted , by default opens it in editable mode.
    if get_tkt['Status']['current'] == 'To Be Accepted' and str(request.user) == get_tkt['Raised_By_id']:
        form_html = editable_ticket(request,get_tkt)
        return JsonResponse({'modal_html':form_html,'heading':'Edit Ticket'})

    related_comments = comments_model.objects.filter(for_ticket_id_id=tkt_id)
    
    ordered_tkt = {}
    desc = get_tkt['Description']                   #description consists of the frt fields and values entered by the user

    del get_tkt['Description']
    del get_tkt['is_accepted']

    temp = list(get_tkt.items())                    #slicing the dict object at title so as to re-order the fields to display
    dict1 = dict(temp[:3])
    dict2 = dict(temp[3:])

    if 'modified_at' in desc:
         dict2['Modified At'] = desc['modified_at']
         del desc['modified_at']

    ordered_tkt.update(dict1)                       #finally , arranging the fields in structured and meaningful format
    ordered_tkt.update(desc)
    ordered_tkt.update(dict2)

    allowed_user = False

    #to check if the incoming user is allowd to reply to the ticket or not
    if str(request.user) == get_tkt['Raised_By_id'] or str(request.user) == get_tkt['Accepted_By'] or request.user.is_hod:
         allowed_user = True
         
    #html content that will render the ticket for replies b/w raised,accepted and hod users
    respond_html = Template( '''
        <form method="post" action="{% url 'handle_submit' get_tkt.Ticket_ID %}">
            {% csrf_token %}
              <div class="input_container">
                {% for each_field,value in get_tkt.items %}
                  <div class="input-group mb-3">  
                        {% if each_field == 'Status' and value.current == 'To Be Accepted' and user != get_tkt.Raised_By_id and request.user.can_accept_tickets %}
                            <button class="btn btn-danger" type="button">Accept This Ticket
                            <input type="checkbox" class="form-check-input" name="Status" required />
                            </button>
                        {% else %} 
                            {% if each_field == 'Status' and value.current == 'To Be Accepted' %}
                                <div class="tkt_field">
                                <button style="border-radius: 7px 8px 0 0;" class="btn btn-danger" type="button">
                                {{each_field}}
                                </button>
                             <div class="border border-warning rounded-bottom" style="width:450px;"><b>{{value.current|linebreaks}}</b></div>
                            </div>
                            {% else %}
                                {% if each_field == 'Status' %}
                                <div class="tkt_field">
                                <b style="color:red;">{{each_field}}</b>
                                </button>
                                <p class="text-{{value.colour}}">{{value.current}}</p>
                                {% elif each_field != 'is_closed'%}
                                 <div class="tkt_field">
                                <button style="border-radius: 7px 8px 0 0;" class="btn btn-secondary" type="button">
                                {{each_field}}
                                </button>
                                <div class="border border-info rounded-bottom" style="width:450px;border-top-right-radius:7px;"><b>{{value|linebreaks}}</b></div>
                                </div>
                                {% endif %}
                            </div>
                            {% endif %}
                        {% endif %} 
                        </div>
                  {% endfor %}
                    {% for each_reply in replies %}
                        <button style="margin-left:0%;border-radius: 7px 8px 0 0;" class="btn btn-outline-danger" type="button">
                                {{each_reply.commented_By_id}} - {{each_reply.commented_By_id.name}} @{{each_reply.created_at}}
                                </button>
                             <div class="border border-warning rounded-bottom" style="width:450px;margin-bottom:25px;border-top-right-radius:7px;"><b>{{each_reply.response|linebreaks}}</b></div>
                            </div>
                    {% endfor %}
                    {% if not get_tkt.is_closed %}
                    {% if can_accept and get_tkt.Raised_By_id != user and get_tkt.Accepted_By == 'To Be Accepted' or allowed_user %}
                  <div class="input-group mb-3" style="margin-top:25px;">  
                     <button class="btn btn-primary" type="button">Reply</button>
                     <textarea type="text" class="form-control" name="reply" maxlength="500" placeholder="Max upto 500 characters..." required></textarea>
                 </div>
              </div>
            <a href="{% url 'handle_submit' get_tkt.Ticket_ID %}"><button class="btn btn-warning" type="submit" style="margin-top:1%;">Submit</button></a>
            {% if get_tkt.Status.current != 'To Be Accepted' and user == get_tkt.Raised_By_id %}
            <a href="{% url 'close_handler' get_tkt.Ticket_ID %}"><button type="button" class="btn btn-danger" style="margin-top:1%;">Close Ticket</button></a>
            {% endif %}
            {% endif %}
            {% endif %}
            </form>
            '''
    )

    csrf_token = get_token(request)

    form_html = respond_html.render(Context({
         'get_tkt':ordered_tkt,
         'csrf_token':csrf_token,
         'replies':related_comments,
         'user' : str(request.user),
         'can_accept':request.user.can_accept_tickets,
         'allowed_user':allowed_user,
         'request':request,
    }))

    return JsonResponse({'modal_html':form_html,'heading':'Respond Form'})

