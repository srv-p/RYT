"""qrs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from accounts import views

urlpatterns = [
    path('login/',views.render_login_page,name='login'),                     #to render login page
    path('change_password/',views.change_password_form,name='change_password'),   #allows user to change their passwords.
    path('update_password/',views.update_password,name='update_password'),
    path('signin',views.signin,name='signin'),                               #to handle validation and signing in of the user
    path('signout/',views.signout,name='signout'),                           #to sign out user and redirect to login page                               #to render/redirect to home page
    path('',views.home,name='home'),                                         #to render home page of the regular users.        
    path('faqs/',views.FAQs,name="faqs"),                                    #to render FAQs of all depts on request.
    path('about-us/',views.about_us,name="about_us"),                        #to display about-us page
    path('department/page',views.dept_page,name="dept_page"),                #to render dept members home page
    path('modify-permissions/',views.manage_permissions,name='permissions'), #to allows hods to manage permissions to their dept members.
]
