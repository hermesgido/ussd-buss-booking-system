from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ussd_booking.form import *
from . models import *

def login_view(request):
    if request.method =="POST":        
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"username is {username}")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcom..!")
            return redirect(home)
        else:
             messages.error(request, "Login not succesfull..!")
    return render(request, 'login.html')

@login_required
def home(request):
    bookings_total = Booking.objects.all().count()
    busses_total = Bus.objects.all().count()
    today_schedule = Schedule.objects.all().count()
    total_customers = Passenger.objects.all().count()
    
    context = {"bookings_total":bookings_total, "busses_total":busses_total, "today_schedule":today_schedule, "total_customers":total_customers}
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect(home)

def register(request):
    return render(request, 'register.html')

def users(request):
    users_list = User.objects.all()
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            role = form.cleaned_data['role']
            first_name, last_name = full_name.split(' ', 1)
            
            if full_name and email and phone_number and role:
                if User.objects.filter(username=email).exists():
                    messages.error(request, "User already exists")
                    return redirect(users)
            if len(password)< 4:
                messages.error(request, "Passoword is too short")
                return redirect(users)
            if role == "Admin":
                user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name, is_superuser=True)
                user.save()
                messages.success(request, "User saved as Admin Successfull")
                return redirect(users)
            if role == "Manager":
                user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name,  is_staff=True)
                
                user.save()
                messages.success(request, "User saved as Manager Successfull")
                return redirect(users)
            messages.error(request, "Unknown error occurred")
            return redirect(users)
        messages.error(request, "You have entered invalid data")
            
            
    context = {'form': form, 'users': users_list}
    return render(request, 'users.html', context)


def busses(request):
    busses_list = enumerate(Bus.objects.all(), start=1)
    form = BussForm()
    if request.method == 'POST':
        form = BussForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Busses added Successfull")
            return redirect(busses)
        
    
    context =  {'form': form, 'busses_list': busses_list}
    return render(request, 'buses.html', context)

def routes(request):
    routes_list = enumerate(Route.objects.all(), start=1)
    form = RouteForm()
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Routes added Successfull")
            return redirect(routes)
        else:
            form = RouteForm()
    
    context =  {'form': form, 'routes_list': routes_list}
    return render(request, 'routes.html', context)

def bookings(request):
    bookings_list =enumerate(Booking.objects.all(), start=  1)
    print(Booking.objects.all())
    form = BookingForm()
    
    context =  {'form': form, 'bookings': bookings_list}
    return render(request, 'bookings.html', context)


def schedule(request):
    schedule_list =enumerate(Schedule.objects.all(), start=1)
    print(schedule_list)
    form = ScheduleForm()
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
           buss = form.cleaned_data['bus']
           route = form.cleaned_data['route']
           date = form.cleaned_data['date']
           
           if Schedule.objects.filter(bus=buss, date=date):
               messages.error(request, "Schedule with this buss alredy exist")
               return redirect(schedule)
        #    if Schedule.objects.filter(route=route, date=date).exists():
        #        messages.error(request, "Schedule with this route and date alredy exist")
               return redirect(schedule)
           form.save()
           messages.success(request, "Schedule successfully added")
           return redirect(schedule)
    
    context =  {'form': form, 'schedule_list': schedule_list}
    return render(request, 'schedule.html', context)



def complaints(request):
    complaints_list =  enumerate(Complaint.objects.all(), start=1)
    
    context =  {'complaints': complaints_list}
    return render(request, 'complaints.html', context)

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect(users)

def delete_schedule(request, id):
    sch = Schedule.objects.get(id=id)
    sch.delete()
    messages.success(request, 'Schedule deleted successfully')
    return redirect(schedule)


# def delete_user(request):
#     return redirect(users)
# def delete_user(request):
#     return redirect(users)

