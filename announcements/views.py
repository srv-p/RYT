from django.shortcuts import render
from time import strptime
from django.http import *

from django.shortcuts import *
from accounts.views import *
from .models import *
from .forms import *

# Create your views here.
# allows different depts to make announcements and manage them
@login_required(login_url='/login')
def manage_dept_annoucements(request):

    if request.session['user_type'] != 'dept':
        return ('/')
    
    #deletes the expired announcements made by the depts
    delete_expired_announcements(request)

    get_announcements = announcements_model.objects.filter(Department_Name = request.user.dept_name)

    # a variable which checks if the user can make/delete an announcement
    can_accept_tkts = request.user.can_accept_tickets

    # a carousel that will render all the announcements by the user's dept in their dept page
    view_html = Template("""  
        <h1 style='margin-top:3%;'><center>
        {% if not announcements %}
        No announcement made yet !! <br> Make an announcement now as a {{dept_name}} member<br>
        {% if can_accept_tkts %}
               <button type="button" class="btn btn-primary" id="announce" data-toggle="modal" data-target="#modal_html">
               + Make an Announcement
                </button>
         {% endif %}
        {% else %}
        Announcements made by {{dept_name}} Department
         {% if can_accept_tkts %}
            <button type="button" class="btn btn-primary" id="announce" data-toggle="modal" data-target="#modal_html">
            + Make another
            </button>
         {% endif %}
        </center></h1>
        {% endif %}
    <div id="carouselExampleControls" class="carousel slide" style="height:500px;" data-bs-ride="carousel">
          <div class="carousel-inner">
        {% for each_announcement in announcements %}
        <div 
        {% if forloop.last %}
        class="carousel-item active" 
        {% else %}
        class="carousel-item" 
        {% endif %}
        
        style="background-color:#383838;height:500px;position: relative;text-align: center;">
          
          <!-- <img src="/static/imgs/try.png" style="height:500px;" class="d-block w-100" alt="..."> -->
            <div class="announcement_name" style="position: absolute;text-decoration: underline;top: 8%;text-align:center;margin-left: 18.2%;width: 63.5%;font-weight: bolder;font-size: 3vw;color: white;">
              {{each_announcement.Title}}
              {% if can_accept_tkts %}
            <a href="{% url 'delete_announcement' each_announcement.Department_Name each_announcement.Title %}"><i class="fa fa-trash"></i></a>
            {% endif %}
            </div> 
            <div class="dept_name" style="position: absolute;text-align:center;top:25%;right:18.3%;width:22%;font-weight: bold;font-size:1vw;color:yellow">
              Made By {{each_announcement.made_by}}
            </div>

            
            <div class="ann_desc" style="position: absolute;margin-left:18.2%;text-align:center;width:63.5%;top:43%;font-weight:normal;font-size: 1.5vw;color:white;">
              <p><i> {{each_announcement.Announcement}}
                <!-- limit:500 characters -->
              </i></p>
            </div>

            </div>
            {% endfor %}
            </div>
            

            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
            </button>
        </div>

     """)

    view_html = view_html.render(Context({'announcements':get_announcements,'can_accept_tkts':can_accept_tkts,'dept_name':request.user.dept_name}))

    return render(request,'base.html',{'view_html':view_html})

# to display the latest announcements made by diff departments to the users
@login_required(login_url='/login')
def announcements(request):

    # if a dept memeber tries to access the user's page , redirect him back to dept page.
     if 'user_type' in request.session and request.session['user_type'] == 'dept':
        return redirect('/department/annoucements')
    
    #to delete the expired announcements
     delete_expired_announcements(request)
     get_annoucements = announcements_model.objects.all()
     print(type(get_annoucements))

    #html content to render all the announcements in carousel . latest ones will be the first
     view_html = Template("""
             {% if not announcements %}
            <h1 style='margin-top:3%;'><center>No new announcements to display</center></h1>
        {% endif%}
    <div id="carouselExampleControls" class="carousel slide" style="height:500px;" data-bs-ride="carousel">
          <div class="carousel-inner"">
        {% for each_announcement in announcements %}
        <div 
        {% if forloop.last %}
        class="carousel-item active"
        {% else %}
        class="carousel-item" 
        {% endif %}
        style="background-color:#383838;height:500px;position: relative;text-align: center;">

            <div class="announcement_name" style="position: absolute;text-decoration: underline;top: 8%;text-align:center;margin-left: 18.2%;width: 63.5%;font-weight: bolder;font-size: 3vw;color: white;">
              {{each_announcement.Title}}
              <!-- limit:40characters -->
            </div> 

            <div class="dept_name" style="position: absolute;text-align:center;top:25%;right:18.3%;width:22%;font-weight: bold;font-size:1vw;color:yellow">
              Brought to you @ {{each_announcement.Department_Name}}
            </div>

            
            <div class="ann_desc" style="position: absolute;margin-left:18.2%;text-align:center;width:63.5%;top:43%;font-weight:normal;font-size: 1.5vw;color:white;">
              <p><i> {{each_announcement.Announcement}}
                <!-- limit:500 characters -->
              </i></p>
            </div>

            </div>
            {% endfor %}
            </div>

            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
            </button>
        </div>
     """)

     view_html = view_html.render(Context({'announcements':get_annoucements,'dept_name':request.user.dept_name}))
     return render(request,'base.html',{'view_html':view_html})

#to delete the expired announcements
def delete_expired_announcements(request):
    current_time = timezone.now()

    #get all the announcements that are expired.
    expired_announcements = announcements_model.objects.filter(Validity__lte=current_time)
    
    #delete each of them.
    for each_announcement in expired_announcements:
         each_announcement.delete()

    return home(request)

#gets the announcement form when a dept member wants to make an announcement
@login_required(login_url='/login')
def new_announcement_form(request):
     
     announcement_form = Announcement_Form()
    
     modal_html = Template("""
            <form action="{% url 'broadcast' %}" method="POST">
                {% csrf_token %}
                    {{form}}
                <a href="{% url 'broadcast' %}" ><button type="submit" class="btn btn-outline-primary" style="margin-top:10px;">Submit</button></a>
            </form>
     """)

     csrf_token = get_token(request)
     modal_html = modal_html.render(Context({
          'form':announcement_form,
          'csrf_token':csrf_token
     }))

     return JsonResponse({'modal_html':modal_html,'heading':'New Announcement'})

#to store the new announcement made the depts into db
@login_required(login_url='/login')
def create_announcement(request):  

    title = request.POST.get('Title')
    announcement = request.POST.get('Announcement')
    validity = request.POST.get('Validity')

    new_announcement = announcements_model.objects.create(
         Title = title,
         Announcement = announcement,
         Department_Name = request.user.dept_name,
         made_by = request.user,
         Validity = validity,
    )

    return redirect('/manage/announcements/')

#deletes the announcements made by the dept on click of delete button
@login_required(login_url='/login')
def delete_dept_announcement(request,dept,name):
    get_annoucement = announcements_model.objects.get(Q(Department_Name=dept) & Q(Title=name))
    get_annoucement.delete()
    return redirect('/manage/announcements/')