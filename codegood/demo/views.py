from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from .forms import user,login_user,reset_psswrd
from django.template import loader
from .models import user_db,admin_db
import hashlib

# Create your views here.

def validate_password(password):
    special_characters = ['!','@','#','$','%','^','&','*']
    l=len(password)
    if(l >=8 and  l<=20):
        num_count = 0
        upper_count = 0
        lower_count = 0
        special_count = 0
        count = 0
        for i in password :
            if(i.isnumeric()):
                num_count += 1
            elif (i.isalpha()):
                if(i.isupper()):
                    upper_count += 1
                elif(i.islower()):
                    lower_count += 1
            elif i in special_characters:
                special_count += 1
            else:
                count += 1

        if(num_count > 0 and upper_count > 0 and lower_count > 0 and special_count > 0 and count ==0 ):
            return True
        else:
            return False
    else:
        return False

def index(request):
    return HttpResponse("Hello world!")

def register(request):
    context={}
    if (request.method=="GET"):
        context['user']=user()
        return render(request,"registeration.html",context)
    if(request.method=="POST"):
        register_as = request.POST['register_as']
        user_nm = request.POST['user'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        conf_password = request.POST['confirm_password']
        context['user']=user()
        if (register_as != "Select" ) and (len(user_nm) != 0) and (len(email) != 0) and (len(password) != 0) and (len(conf_password) != 0):
            if len(password) == len(conf_password) and password == conf_password:
                if(validate_password(password)):
                    if(register_as=="user"):
                        try:
                            db = user_db.objects.get(user_nm = user_nm)
                            context['error'] = "Username already Exists, enter again"
                            return render(request,"registeration.html",context)
                        except ObjectDoesNotExist:
                            hash_password = hashlib.md5(password.encode()).hexdigest()
                            db = user_db(user_nm = user_nm, password = hash_password, email = email)
                            db.save()
                            return HttpResponse("User Doesn't exist Registering user")
                    else:
                        try:
                            db = admin_db.objects.get(admin_nm = user_nm)
                            context['error'] = "Username already Exists, enter again"
                            return render(request,"registeration.html",context)
                        except ObjectDoesNotExist:
                            hash_password = hashlib.md5(password.encode()).hexdigest()
                            db = admin_db(admin_nm = user_nm,password = hash_password, email = email)
                            db.save()
                            return HttpResponse("User Doesn't exist Registering user")
                else:
                    context['pass_error'] = "Password should contain minimum of 8 characters, maximum of 20 characters, atleast a lower case an an upper case alphabets, a number and a special character among !@#$%^&*, spaces not allowed"
                    return render(request,"registeration.html",context)

            else:
                context['pass_error'] = "Password and Confirm Password doesn't match"
                return render(request,"registeration.html",context)
        if (register_as == "Select" ):
            context['role_error'] = "Select Role as either Teacher or Student to proceed"
        if (len(user_nm) == 0):
            context['user_error'] = "User name cannot be empty"
        if (len(email) == 0):
            context['email_error'] = "Email address cannot be empty"
        if (len(password) == 0):
            context['pass_error'] = "Password cannot be empty"
        if (len(conf_password) == 0):
            context['conf_pass_error'] = "Confirm Password cannot be empty"
        return render(request,"registeration.html",context)


def login(request):
    if (request.method=="GET"):
        context={}
        context['login']=login_user()
        return render(request,"loog.html",context)
    if(request.method=="POST"):
        login_as = request.POST['login_as']
        user_nm = request.POST['user']
        password = request.POST['password']
        context={}
        context['login']=login_user()
        if(login_as != "Select" and len(user_nm) != 0 and len(password) != 0):
            if login_as == "user":
                try:
                    hash_password = hashlib.md5(password.encode()).hexdigest()
                    db = user_db.objects.get(user_nm = user_nm, password = hash_password)
                    return HttpResponse("User login successful")
                except ObjectDoesNotExist:
                    context['error'] = "Invalid Credentials"
                    return render(request,"loog.html",context)
            else:
                try:
                    hash_password = hashlib.md5(password.encode()).hexdigest()
                    db = admin_db.objects.get(admin_nm = user_nm, password = hash_password)
                    return HttpResponse("Admin login successful")
                except ObjectDoesNotExist:
                    context['error'] = "Invalid Credentials"
                    return render(request,"loog.html",context)
        if (login_as == "Select" ):
            context['role_error'] = "Select Role as either Teacher or Student to proceed"
        if (len(user_nm) == 0):
            context['user_error'] = "User name cannot be empty"
        if (len(password) == 0):
            context['pass_error'] = "Password cannot be empty"
        return render(request,"registeration.html",context)

def reset_password(request):
    if (request.method=="GET"):
        context={}
        context['reset']=reset_psswrd()
        return render(request,"passwordReset.html",context)
    if(request.method=="POST"):
        role = request.POST['role']
        user_nm = request.POST['user']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        context={}
        context['reset']=reset_psswrd()
        if(role != "Select" and len(user_nm) != 0 and len(password) != 0 and len(conf_password) != 0):
            if(len(password) == len(conf_password) and password == conf_password):
                if(validate_password(password)):
                    if role == "user":
                        try:
                            hash_password = hashlib.md5(password.encode()).hexdigest()
                            db = user_db.objects.filter(user_nm = user_nm).update(password = hash_password)
                            return HttpResponse("Password Reset successful")
                        except ObjectDoesNotExist:
                            context['error'] = "Invalid User to reset password"
                            return render(request,"loog.html",context)
                    else:
                        try:
                            hash_password = hashlib.md5(password.encode()).hexdigest()
                            db = admin_db.objects.filter(admin_nm = user_nm).update(password = hash_password)
                            return HttpResponse("Password Reset successful")
                        except ObjectDoesNotExist:
                            context['error'] = "Invalid User to change password"
                            return render(request,"loog.html",context)
                else:
                    context['error'] = "Password should contain minimum of 8 characters, maximum of 20 characters, atleast a lowercase and an upper case alphabet, a number and a special character among !@#$%^&*, spaces not allowed"
                    return render(request,"passwordReset.html",context)
            else:
                context['error'] = "New Password and Confirm Password doesn't match"
                return render(request,"passwordReset.html",context)
        if (role == "Select" ):
            context['role_error'] = "Select Role as either Teacher or Student to proceed"
        if (len(user_nm) == 0):
            context['user_error'] = "User name cannot be empty"
        if (len(password) == 0):
            context['pass_error'] = "Password cannot be empty"
        if (len(conf_password) == 0):
            context['conf_pass_error'] = "Confirm Password cannot be empty"
        return render(request,"passwordReset.html",context)