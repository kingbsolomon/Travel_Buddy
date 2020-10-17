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
        user = User.objects.get(username = x['username'])
        request.session['name'] = user.name
        request.session['username']= user.username
        request.session['id'] = user.id
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
        user = User.objects.get(username=request.POST['username'])
        if user:
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['name'] = user.name
                request.session['username']= user.username
                request.session['id']= user.id
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
            my_trips = User.objects.get(id=request.session['id']).planner.all()
            my_joins = User.objects.get(id=request.session['id']).trips.all()
            not_my_trips = Trip.objects.exclude(users_joining= request.session['id']).exclude(planned_by = request.session['id'])
            context = {
                "my_trips" : my_trips,
                "my_joins" : my_joins,
                "not_my_trips": not_my_trips,
            }
            return render(request, 'travels.html', context)
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
        user_planned_by = User.objects.get(id=request.session['id'])
        Trip.objects.create(destination = x["destination"], planned_by = user_planned_by, 
        travel_start = x['travel_start'], travel_end = x['travel_end'], desc = x['desc'])
        return redirect('/success')

def view_trip(request, tripid):
    trip_info= Trip.objects.get(id=tripid)
    trip_status = ""
    if request.session['id'] == trip_info.planned_by.id:
            trip_status = "planner"
    else:
        for user in trip_info.users_joining.all():
            if request.session['id'] == user.id:
                trip_status = "buddy"
                break
            else:
                trip_status = "none"
    
    context = {
        "trip_info": trip_info,
        "trip_status": trip_status
    }
    return render(request, 'destination.html',context)

def join_trip(request,tripid):
    user = User.objects.get(id=request.session['id'])
    Trip.objects.get(id=tripid).users_joining.add(user)
    return redirect('/success')

def del_trip(request,tripid):
    trip_del = Trip.objects.get(id=tripid)
    if trip_del.planned_by.id == request.session['id']:
        trip_del.delete()
    return redirect('/success')

def unjoin(request,tripid):
    trip_unjoin = Trip.objects.get(id=tripid)
    user = User.objects.get(id=request.session['id'])
    try:
        trip_unjoin.users_joining.remove(user)
        return redirect('/success')
    except:
        return redirect('/success')

def edit(request, tripid):
    context = {
        'trip_info': Trip.objects.get(id=tripid),
    }
    return render(request, 'edit.html', context)

def update(request, tripid):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect(f'/edit/{tripid}')
    else:
        trip_to_update = Trip.objects.get(id=tripid)
        trip_to_update.destination = request.POST['destination']
        trip_to_update.desc = request.POST['desc']
        trip_to_update.travel_start = request.POST['travel_start']
        trip_to_update.travel_end = request.POST['travel_end']
        trip_to_update.save()
        return redirect(f'/view_trip/{tripid}')