import datetime

from django.shortcuts import *
from django.template import Template,Context
from django.contrib.auth.forms import PasswordChangeForm
from django.middleware.csrf import get_token
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from raise_tktapp.models import *
from announcements.models import *
from django.db.models import Q
from .forms import *

#to redirect user to their respective home pages based on login types.
def login_redirection(request,user_type):
        
        if user_type == 'dept':                     #if login type is as department member , redirect to department home page
            return redirect('department/page')
        
        elif request.is_superuser:                  #if user is admin , redirect to admin page
            return redirect('/admin/')

        return redirect('/')                        #else redirect to user home page

@login_required(login_url='/login')                 #lets user change their passwords.
def change_password_form(request,*args):
            
            msg = ''
            if args:
                 msg = args[0]

            form = PasswordChangeForm(user=request.user)        #this is in-built password change form of django.

            csrf_token = get_token(request)                     #to generate a csrf token for the form.

            view_html = Template("""
            <div class="border border-success border-3" style="margin:3%;padding:5%;">
            <h1 style="font-family:serif;margin-bottom:3%;"><center>Password Change</center></h1>
            <div class="form_container" style="margin-left:25%;margin-top:2%;">
                    <form action={% url 'update_password' %} method="post">
                        {%csrf_token%}
                        {{form.as_p}}
                        {% if msg != '' %}
                            <h4 style="color:red;">{{msg}}</h4>
                        {% endif%}
                        <a href="{% url 'update_password' %}"><button class="btn btn-warning" style="margin-left:22%;margin-top:2%;">Save Changes</button></a>
                    </form>
                </div>
                </div>
                """)
                
            #rendering the content in modal_html as html content.
            view_html  = view_html.render(Context({'view_html':view_html,'csrf_token':csrf_token,'form':form,'msg':msg}))

            #returned to #change_password click function in myJS.js 
            return render(request,'base.html',{'view_html':view_html})  

@login_required(login_url='/login') 
def update_password(request):
        if request.method == "POST":
            form = PasswordChangeForm(user=request.user,data=request.POST)
            # print(form)
            if form.is_valid():
                form.save()
                logout(request)
                msg = 'Your sessions has expired. Login with new credentials'
                return render_login_page(request,msg)
            
            else:
                 msg = 'Entered values does not meet required criterion. Please re-enter'
                 return change_password_form(request,msg)
        
#to render login page 
def render_login_page(request,*args):
     
     if request.user.is_authenticated:              #if user is already logged in  , redirect to home page
        return redirect('/')
     
     form = loginForm()
     msg = ''
     if args:
          msg = args[0]
     return render(request,'login.html',{'form':form,'msg':msg})

#to validate user details and login them.
def signin(request):

    if request.user.is_authenticated:               #if already logged in , redirect to home page
        return redirect('/')
    
    form = loginForm()
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('userID')
            pwd = form.cleaned_data.get('password')
            user_type = request.POST.get('user_type')
            request.session['user_type'] = user_type                #storing the login_type as dept/user in session object so as to use it further.

            user = authenticate(request,userID=id,password=pwd)     #in-built function of django to authenticate the user.
            
            if user is not None:                                    #if authenticate finds a user with entered details login him using the login(in-built) func
                login(request,user)
                return login_redirection(user,user_type)
            
            else:                                                   #else , print the message invalid credentials
                msg = 'Invalid Credentials! Please try again.'
                return render(request,'login.html',{'form':form,'msg':msg})

#to render regular user home page. Accessible iff the user is logged in , which is handled by @login_required decorator of django
@login_required(login_url='/login')
def home(request):

    if request.session['user_type'] == 'dept':          #if user type is as dept member , redirect him to dept home page if he tries to access normal user home page.
        return redirect('/department/page')

    replies = 0 

    #to count the number of tickets which has new replies raised by the user
    replies_for_his_tkts = ticket_model.objects.filter(Q(Raised_By_id=request.user))

    for each_tkt in replies_for_his_tkts:

        #if the last reply is not by the user, ie if its the dept member , then increase no.of new replies count by one
        if not each_tkt.is_closed:
            if 'last_commented_by' in each_tkt.Status and each_tkt.Status['last_commented_by'] != str(request.user):
                # print(each_tkt.Status['last_commented_by'])
                replies = replies + 1

    current_time = datetime.datetime.now()
    one_day_ago = current_time - datetime.timedelta(days=1)
    new_announcements = announcements_model.objects.filter(Created_At__gte=one_day_ago).count()

    return render(request,'home.html',{'user':request.user,'new_replies':replies,'new_announcements':new_announcements})

#to render dept home page. Accessible iff the user is logged in , which is handled by @login_required decorator of django
@login_required(login_url='/login')
def dept_page(request):

    if not request.user.is_authenticated:
        return redirect('/login/')
    
    #if the user_type is user , he is not of dept member , so if he tries to access this page , redirect him to normal user home page.
    if 'user_type' in request.session and request.session['user_type'] == 'user':
        return redirect('/')

    #count the number of new tkts of user's department which are not raised by himself to his dept.
    dept_tkts = ticket_model.objects.filter(Q(Department_Name=request.user.dept_name) & Q(Accepted_By='To Be Accepted'))
    dept_tkts = dept_tkts.exclude(Raised_By_id=str(request.user)).count()

    #to count the no.of new replies to the tickets in progress.
    replies_for_dept_tkts = ticket_model.objects.filter(Q(Department_Name=request.user.dept_name))

    for each_tkt in replies_for_dept_tkts:

        #count only if the ticket status is in progress.
        if each_tkt.Accepted_By == str(request.user) and not each_tkt.is_closed:
            if 'last_commented_by' in each_tkt.Status and each_tkt.Status['last_commented_by'] != str(request.user):
                # print(each_tkt.Status['last_commented_by'])
                dept_tkts = dept_tkts + 1
                # print(dept_tkts)

    return render(request,'dept.html',{'new_tkts_and_replies':dept_tkts})

#to redirect to login page after loggout
def signout(request):
    logout(request)
    return redirect('/login/')

#to allow hods of the dept to manage permissions to their dept members like ticket acceptance and frt handlings.
@login_required(login_url='/login')
def manage_permissions(request):

        msg = ''

        if request.method == "POST":                    
            id = request.POST.get('userID')
            can_accept_tickets = request.POST.get('can_accept_tickets')
            can_modify_frts = request.POST.get('can_modify_frts')
            get_user = User.objects.get(userID=id)

            if can_accept_tickets == 'on':              #if this option is checked by the hod , update the permission for the user.
                get_user.can_accept_tickets = True

            else:
                get_user.can_accept_tickets = False     #else remove the permission.

            if can_modify_frts == 'on':
                get_user.can_modify_frts = True

            else:
                get_user.can_modify_frts = False
    
            #save the changes to the members in database.
            get_user.save(update_fields=['can_modify_frts','can_accept_tickets'])
            msg = 'Successfully updated the permissions for the user with ID ' + id

        #fetches the details of the dept members of the hod's dept
        dept_memebers = User.objects.filter(dept_name = request.user.dept_name).only('userID','name','student_year','can_accept_tickets','can_modify_frts','is_hod').values('userID','name','student_year','can_accept_tickets','can_modify_frts','is_hod')

        csrf_token = get_token(request)
        
        #form to allow hods to manage permissions to their dept members.
        permissions_html = Template("""
                    <h1 style="margin-top: 3%;margin-bottom:3%;font-family:Bodoni MT;text-align: center;font-weight: 20%;">
                    Manage {{dept_name}} Department Permissions</h1>
                    {% for each_member in dept_memebers %}
                        <div class="x" style="margin:2%;">
                        <form style="margin-left:3%;" action="{% url 'permissions' %}" method="post">
                        {%csrf_token%}
                        <input type="text"  style="margin-left:5%;display:inline-block;text-align:center;width:8%;" name="userID" value="{{each_member.userID}}" readonly class="form-control" />
                        <input type="text"  style="margin-left:2%;display:inline-block;text-align:center;width:fit-content;" value="{{each_member.name}}" readonly class="form-control" />
                        <label style="margin-left:3%;" for="can_accept_tickets">Can Accept Tickets</label>
                        <input style="margin-top:1%;" type="checkbox"  {% if each_member.can_accept_tickets %} checked {% endif %} name="can_accept_tickets" class="form-check-input" />
                        <label style="margin-left:2%;" for="can_modify_frts">Can Modify Frts</label>
                        <input style="margin-top:1%;" type="checkbox"  {% if each_member.can_modify_frts %} checked {% endif %} name="can_modify_frts" class="form-check-input" />
                        <button style="margin-left:3%;" type="submit" class="btn btn-warning">Save Changes</button>
                        </form>
                        </div>
                    {% endfor %} 

                    {% if msg != '' %}
                    <script>
                        window.alert("{{msg}}")
                    </script>
                    {% endif %}
            """)

        permissions_html = permissions_html.render(Context({'dept_name':request.user.dept_name,'dept_memebers':dept_memebers,'csrf_token':csrf_token,'msg':msg}))
        return render(request,'base.html',{'view_html':permissions_html})

#to render frequently asked questions on each dept.
@login_required(login_url='/login')
def FAQs(request):
     
     if not request.user.is_authenticated:
         return redirect('/login/')
     
     #a nested dictonary that stores each dept as key which in turn has faq and its ans as key value pairs.
     dept_faqs = {
          
          'Altar':{
        'Can I give aarthi to Swami?':'Indeed. Raise a ticket and discuss with us to fix the date.',

        'What are the bell timings?':'''
            05:15 am - 21 Bells     
            05:35 am - Warning bell: Suprabhatam    
            06:10 am - Warning bell: Jogging    
            08:15 am - Breakfast    
            08:55 am - Long Bell    
            09:05 am - Warning bell: Institute Prayer   
            12:20 pm - Lunch    
            01:10 pm - Warning bell: Classes resume     
            04:00 pm - Snacks   
            06:00 pm - Long Bell    
            06:05 pm - Vedam    
            06:25 pm - Warning bell: Bhajans    
            07:15 pm - Dinner   
            07:50 pm - Warning bell: Study Hours    
            08:00 pm - Study Hours      
            09:30 pm - Study Hours End      
            10:00 pm - Warning bell: Retire     
            10:10 pm - Good Night! LightsOFF!  
        ''',

        'Can I perform pooja during festivals?':'Yes, indeed. Please raise a ticket to get more details.',

    },

          'Ankur':{ 
        'Can I grow a particular type of plant?':'Ofcourse, raise a ticket and discuss in detail with us.',

        'Do I have an option to explore more about gardening?':'Absolutely, raise a ticket to learn more.',

        'Am I allowed to rent gardening tools?':'Very well, you can. Raise a ticket to rent the tools.',

        'Can I know the variety of plants present in our campus?':'Yes! Raise a ticket to know now.',

    },

          'Aura':{ 
       
        'What is the cost of new issue card?':'Rs. 20 should be paid in cash.',

        'What is the cost of renting an Academic book?':"The cost depends on the book's price, raise a ticket for more details.",

        'How many books can I issue at once?':'At one time, a student can issue 1 book',

        'What is the duration until which I can keep a rented book with me?':'For the entire semester',

        'What is the duration until which I can keep an issued book with me?':'For one week & it can be extended to another week',

        'What is the fine imposed on me for not returning a book on time?':'Rs 5 a day',

        'Can I request Aura department to buy a book that I want to read?':'Yes you can, please raise a ticket for more details.',

        'Can I know whether a particular book is available in Aura or not':'Raise a ticket to get know about your favourite book.',

    },

          'Cardroom':{ ### other questions needed
        'Can I share my ideas for making a card?':'Yes, you may share your creative thoughts by raising a ticket.',

        'May I offer help when people are making a card?':'We definitely need helping hands. You will be informed when we start making a card in Accouncements corner.',

    },

          'Holistic_Health':{ #h2 timings and any other tickets
        'When is the doctor expected to come?':'Usually the doctor visits thrice a week. Typically Monday , Thursday and Saturday around 4:30 pm to 5:00 pm. Any changes will be announced',

        'Timings of H2':'Morning : 8:30 - 9:00 , Evening : 7:10 - 7:30 , Night : 9:30 - 9:45',

        'I think I\'m suffering from an illness. What should I do?':'Please visit H2 department room (A20) in the hostel or raise a ticket.',

        'Can I place an order for medicines?':'Definitely. Get in touch with us by raising a ticket.',

    },

          'Hostel_Essentials':{#other ques
         
        'Laundry Timings':'4 times in a month.Exact Timings will be announced one day prior.',#timings
    
        'How do I enquire about my missing clothes?':'Please raise a ticket to discuss about the issue in detail.',

        'When is the next HSBC Recharge Date?':'HSBC Recharge is done on every Monday, Wednesday and Saturday.',

        'When will the Trimmer Charging be done?': 'Typically , Wednesday and Friday of every week.', ##### timings

        'My chair is broken. What should I do now?':'You will have to pay a fine of Rs. 500. You may contact us through a ticket for more details.',

        'My cupboard keys are missing. What should I do now?':'There will be a fine of Rs.100. You may raise a ticket to get your issue resolved.',

        'Tailor Visits':'Twice a month. Based on requirements.',

        'Barber Vistis':'Generally , Wednesday and Sunday of every week. Subject to change as per requirement.'

    },

          'InSaight':{#other ques
        'When is the next article being published?':'We publish articles once in a month,will announce the date in the Announcements corner when we\'re ready with our article.',

        'Where am I supposed to submit my creative writings and photos?':'mail us bro', #email id

    },

          'Kitchen':{#table for first two
        'What are the meal timings?':['is_image','../media/faqs/meals-time.jpg'],

        'What are the Serving Batch timings?':'''
             Meal         1st Serving Batch       2nd Serving Batch      
           Breakfast     08:10 am - 08:35 am     08:35 am - 08:50 am     
               Lunch     12:15 pm - 12:35 pm     12:35 pm - 12:55 pm     
              Dinner     07:10 pm - 07:30 pm     07:30 pm - 07:50 pm    
        ''', 

        'Where do I provide food feedback?':'We welcome all the suggestions and complaints. You may raise a ticket and provide feedback.',

        'Can I provide food suggestions for special dinners?':'Yes, you may raise a ticket and suggest food items. (But the ticket window for this issue will be opened temporarily)', #####
    
    },

          'Maintenance':{
        'My cupboard/ tubelight/ window mesh is damaged. What should I do?':'Raise a ticket and tell us your room details.',

        'Can I provide song suggestions for Sunday mornings?':'Yes, you may raise a ticket and suggest some songs. (But the ticket window for this issue will be opened temporarily)', #####
    
        'Where can I share festival decoration ideas?':"You're at the right place. Raise a ticket to share now.",
    },

          'Multimedia':{
        'When can I get access to photos and videos of this semester?':'At the end of the semester via D2H (Data to Home).',

        'Where can I share new ideas for pre-movie/creative videos':'Raise a ticket & share with us to work together for the best outcome.',

        'Where can I give feedback on the latest videos made by the department':'We respect and value your feedback & suggestions. Feel free to raise a ticket and discuss with us.',

    },

          'Music':{
        'Can I learn a musical instrument?':'Indeed, you may raise a ticket to talk to us in detail.',

        'Where can I share my idea(s) on planning an event\'s musical performance?':'Please raise a ticket to share your ideas with us.',

        'Can I provide bhajans suggestions?':'Yes, you may raise a ticket and suggest some bhajans. (But the ticket window for this issue will be opened temporarily)',

    },

          'Sai_Replica':{#any other ques
        'How to place an order for a printout?':'''
        Step 1: Login to the HSBC page: http://192.168.34.5:8080/HSBC/login.jsp
        Step 2: Click on --> 'Sai Replica' --> 'Place Order' 
        Step 3: Check whether your file is in the Sai Replica cloud.
        Step 4: If the file is present there, you may select the file and place an order.
        Step 5: If not present, then meet a department member physically and ask him to upload the files. He shall guide you further.
        ''',

        'Can I complaint about wrong amount deduction?':'By all means. Raise a ticket to complaint, we will definitely resolve.',

        'How long will it take for the printout to be taken once I place an order?':'Anywhere between 1-5 days', #confirm this
        
    },

          'Sports':{#any other ques & clarify
         
        'Gym Room Timings':'',#find out

        'I want to start a new fitness routine. Can I get guidance?':'Absolutely. You may raise a ticket and discuss in detail with us.',

        'Where can I get new sports equipment?':'We undertake your personal sports equipment orders. You may raise a ticket and place an order.',

        'If I fall sick, how can I get exemption from Jogging Session':'Write a letter to PT Sir & Warden Sir which is acknowledged by the room leader. For any other details, raise a ticket now.',

    },

          'Stores':{
         
        'Stores Timings':'''
        Mon-Sat: 04:30pm - 05:00pm
        Sun:     10:30am - 11:00am
        ''',

        'Menu for Special orders':['is_image','../media/faqs/stores-menu.png'],

        'Special Items Schedule':'''
        Monday: Bakery
        Tuesday: Ice-creams/cold drinks
        Wednesday: Bakery
        Thursday: Ice creams
        Friday: Bakery
        Saturday: Fruits/Ice-creams
        Sunday: Ice creams/cold-drinks
        ''', #will find

        'Can I place personal orders?':'We undertake personal orders. Raise a ticket and talk to us for more details.',

        'How to check my Transaction details?':'''
        Step 1: Login to the HSBC page: http://192.168.34.5:8080/HSBC/login.jsp
        Step 2: Click on --> 'Stores' --> 'Reports Page' --> 'Generate Reports'
        Step 3: A transaction list will be displayed. Click on each transaction for more details.
        ''',

        'If my transaction went wrong, how can I resolve it?':'Raise a ticket & share the details to get your issue resolved.',

        'Where can I place order for Room Party or Department Party?':'Raise a ticket and provide the details to place your order.',

    },

          'Telephone':{
         
        'Telephone Slot Timings':'You can find out in Hostel Notice Board.',

        'How to get my personal phone?':'If there is a need of your personal phone, you may take Warden Sir\'s permission. ',

        'How to complaint about landlines?':'You can raise a ticket and register a complaint. We\'ll definitely look into it.',

        'How can I change my registered number?':'You can raise a ticket and provide details to help you out.',


         }
     }

     #html content that renders the above faqs
     faq_html = Template("""
        <div class="faq_head" style="text-align:center;font-size:2rem;margin:2%;font-weight:30px;font-family:Bellota Text;">
            <h1 style="font-family:Bellota Text;">Frequently Asked Questions</h1> 
        </div>
            <div class="container-fluid">
      <div class="accordion" id="accordionExample">
        {% for dept_name,faqs in dept_faqs.items %}
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" id="dept" type="button" data-bs-toggle="collapse" data-bs-target="#{{dept_name}}" aria-expanded="false" aria-controls="collapseOne"> {{dept_name}} </button>
            </h2>
            <div id="{{dept_name}}" class="accordion-collapse collapse" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                {% for faq,soln in faqs.items %}
                  <div class="accordion-item">
                    <h2 class="accordion-header" >
                        <button class="accordion-button collapsed" id="faq" type="button" data-bs-toggle="collapse" data-bs-target="#{{dept_name}}-{{forloop.counter}}" aria-expanded="false"> {{faq}} </button>
                    </h2>
                    <div id="{{dept_name}}-{{forloop.counter}}" class="accordion-collapse collapse">
                        {% if soln.0 == 'is_image' %}
                        <img src="{{soln.1}}" style="margin:3%;"/>
                        {% else %}
                        <div class="accordion-body">{{soln|linebreaksbr|safe}}</div>
                        {% endif %}
                    </div>
                  </div>
                  {% endfor %}
                </div>
            </div>
        </div>
        {% endfor %}
        </div>
        </div>
     """)

     faq_html = faq_html.render(Context({"dept_faqs":dept_faqs}))

     return render(request,'base.html',{'view_html':faq_html})

@login_required(login_url='/login')
def about_us(request):
    return render(request,'about_us.html')