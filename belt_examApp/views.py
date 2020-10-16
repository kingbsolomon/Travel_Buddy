from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
            messages.set_level(request, messages.ERROR)
        return redirect('.')
    else:
        x = request.POST
        pw_hash = bcrypt.hashpw(x['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(name = x['name'], username = x['username'], password = pw_hash)
        request.session['name'] = f"{x['name']}"
        request.session['username']= f"{x['username']}"
        request.session['auth_user']= True
        return redirect('/success')
        
def login(request):
    errors_login = User.objects.login_validator(request.POST)
    if len(errors_login) > 0:
        for key,value in errors_login.items():
            messages.warning(request,value)
            messages.set_level(request, messages.WARNING)
        return redirect('.')
    else:
        user = User.objects.filter(username=request.POST['username'])
        if user:
            if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
                request.session['name'] = f"{user[0].name}"
                request.session['username']= f"{user[0].username}"
                request.session['auth_user']= True
                return redirect('/success')
            else:
                errors_login['login'] = "Invalid Email/Password Combination"
                for key,value in errors_login.items():
                    messages.warning(request,value)
                    messages.set_level(request, messages.WARNING)
                return redirect('.')
        else:
            errors_login['login'] = "User does not exist. Please Register."
            for key,value in errors_login.items():
                messages.warning(request,value)
                messages.set_level(request, messages.WARNING)
            return redirect('.')

def success(request):
    try:
        if request.session['auth_user'] == True:
            my_trips = User.objects.get(username=request.session['username']).planner.all()
            my_joins = User.objects.get(username=request.session['username']).trips.all()
            id_mytrips = [e.id for e in my_trips]
            id_myjoins = [e.id for e in my_joins]
            combined_list = set(id_myjoins)- set(id_mytrips)
            combined_exclude = id_mytrips + list(combined_list)
            not_my_trips = Trip.objects.exclude(id__in=combined_exclude)
            context = {
                "my_trips" : my_trips,
                "my_joins" : my_joins,
                "not_my_trips": not_my_trips,
            }
            return render(request, 'travels.html',context)
    except:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def add_trip(request):
    return render(request, 'add_trip.html')

def create_trip(request):
    print(request.POST)
    errors_trip = Trip.objects.trip_validator(request.POST)
    if len(errors_trip) > 0:
        for key,value in errors_trip.items():
            messages.warning(request,value)
            messages.set_level(request, messages.WARNING)
        return redirect('/add')
    else:
        x = request.POST
        user_planned_by = User.objects.get(username=request.session['username'])
        Trip.objects.create(destination = x["destination"], planned_by = user_planned_by, 
        travel_start = x['travel_start'], travel_end = x['travel_end'], desc = x['desc'])
        return redirect('/success')

def view_trip(request, tripid):
    context = {
        "trip_info": Trip.objects.get(id=tripid)
    }
    return render(request, 'destination.html',context)

def join_trip(request,tripid):
    user = User.objects.get(username=request.session['username'])
    Trip.objects.get(id=tripid).users_joining.add(user)
    return redirect('/success')
