from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from .forms import user,login_user
from django.template import loader
from .models import user_db,admin_db

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

def register(request):
    context={}
    if (request.method=="GET"):
        context['user']=user()
        return render(request,"registeration.html",context)
    if(request.method=="POST"):
        register_as = request.POST['register_as']
        user_nm = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['confirm_password']

        print(user_nm,email,password,conf_password)
        if(register_as=="user"):
            try:
                db = user_db.objects.get(user_nm = user_nm)
                context['error'] = "Username already Exists, enter again"
                context['user']=user()
                return render(request,"registeration.html",context)
            except ObjectDoesNotExist:
                db = user_db(user_nm = user_nm,password = password, email = email)
                db.save()
                return HttpResponse("User Doesn't exist Registering user")
        else:
            try:
                db = admin_db.objects.get(admin_nm = user_nm)
                context['error'] = "Username already Exists, enter again"
                context['user']=user()
                return render(request,"registeration.html",context)
            except ObjectDoesNotExist:
                db = admin_db(admin_nm = user_nm,password = password, email = email)
                db.save()
                return HttpResponse("User Doesn't exist Registering user")


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