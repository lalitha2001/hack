from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from .forms import user,login_user
from django.template import loader
from .models import user_db,admin_db

# Create your views here.

def validate_password(password):
    special_characters = ['!','@','#','$','%','^','&','*']
    if(len(password)>=8):
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
        if (len(register_as) != 0) and (len(user_nm) != 0) and (len(email) != 0) and (len(password) != 0) and (len(conf_password) != 0):
            if len(password) == len(conf_password) and password == conf_password:
                if(validate_password(password)):
                    if(register_as=="user"):
                        try:
                            db = user_db.objects.get(user_nm = user_nm)
                            context['error'] = "Username already Exists, enter again"
                            return render(request,"registeration.html",context)
                        except ObjectDoesNotExist:
                            db = user_db(user_nm = user_nm,password = password, email = email)
                            db.save()
                            return HttpResponse("User Doesn't exist Registering user")
                    else:
                        try:
                            db = admin_db.objects.get(admin_nm = user_nm)
                            context['error'] = "Username already Exists, enter again"
                            return render(request,"registeration.html",context)
                        except ObjectDoesNotExist:
                            db = admin_db(admin_nm = user_nm,password = password, email = email)
                            db.save()
                            return HttpResponse("User Doesn't exist Registering user")
                else:
                    context['pass_error'] = "Password should contain minimum of 8 characters, atleast an alphabet, a number and a special character among !@#$%^&*"
                    return render(request,"registeration.html",context)

            else:
                context['pass_error'] = "Password and Confirm Password doesn't match"
                return render(request,"registeration.html",context)
        else:
            context['input_error'] = "Please enter all fields"
            return render(request,"registeration.html",context)



def login(request):
    print(request.method)
    if (request.method=="GET"):
        context={}
        context['login']=login_user()
        return render(request,"loog.html",context)
    if(request.method=="POST"):
        login_as = request.POST['login_as']
        user_nm = request.POST['user']
        password = request.POST['password']
        print(login_as,user_nm,password)
        if(login_as=="user"):
            try:
                db = user_db.objects.get(user_nm = user_nm, password = password)
            except ObjectDoesNotExist:
                return HttpResponse("User Doesn't exist to login")
            return HttpResponse("User login successful")
        else:
            try:
                db = admin_db.objects.get(user_nm = user_nm, password = password)
            except ObjectDoesNotExist:
                return HttpResponse("User Doesn't exist to login")
            return HttpResponse("Admin login successful")

def reset_password(request):
    return HttpResponse('Password Reset')