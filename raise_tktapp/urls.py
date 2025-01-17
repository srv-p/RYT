from .views import *
from django.urls import path
from .dept_views import *

urlpatterns = [  

    path('frt/create_frt',new_frt_create,name="create_frt"),                #renders new frt form for creation by hods.

    path('frt/',frt_page,name='frt_page'),                                  # to allow hods to manage their dept frts

    path('update/<tkt>/<ack>/',update_frt,name='modify_frt'),               # to change availability status of the frt tkt or delete it.

    path('departments/',tkts_departments_page,name='dept_page'),            # to display list of departments to raise a ticket.

    path('departments/<check_dept>/',get_dept_frts,name='frts'),            # to display the frts of particular dept on request.

    path('new_ticket/',raise_tkt,name="raise_tkt"),                         # to handle the submittion of ticket form on raising a ticket .

    path('modify-tkt/',before_accept_handler,name='before_accept_handler'),

    path('close_tkt/<tkt_id>/',close_handler,name='close_handler'),      # to close a ticket raised by a user.

    path('respond/<tkt_id>/',respond_form,name='respond_form'),             # to allow user to reply for a ticket takes tkt_id as parameter.

    path('handle_form/<tkt_id>/',response_handler,name='handle_submit'),    # to store the reply of the user for a ticket.

    path('get_tkts/<for_his_dept>',fetch_user_tkts,name='my_tkts') ,    # to display user raised/department tickets on request.

    path('departments/<dept_name>/<tkt_name>/',get_form,name='raise_frt_tkt'),  # gets the raise_tkt form of selected frt on click.

   
]