from django.contrib.auth.base_user import BaseUserManager

#this class extends django default Base User Manager class to handle user account creation
class CustomUserManager(BaseUserManager):

    #a function to create a user
    def _create_any_user(self, userID,name,dept_name, password,is_superuser,is_staff,is_hod,can_accept_tickets,can_modify_frts,is_active):
       
        if not userID:
            raise ValueError(("Not a valid userID"))
        user = self.model(
            userID=userID,
            name=name,
            dept_name=dept_name,
            is_superuser=is_superuser,
            is_hod = is_hod,
            is_staff = is_staff,
            can_modify_frts = can_modify_frts,
            can_accept_tickets = can_accept_tickets,
            is_active=is_active
        )
        user.set_password(password)
        user.save()
        return user

    #this func calls above func to create account for a normal user
    def create_regular_user(self, userID,dept_name,name, password,is_hod,can_accept_tickets,can_modify_frts):
        return self._create_any_user(userID, name, dept_name, password, False,False,is_hod,can_accept_tickets,can_modify_frts,True)
    
    #this func is to create account for a superuser.
    def create_superuser(self, userID,name, password,is_hod):
        return self._create_any_user(userID, name, '', password, True,True,is_hod,False,False,True)