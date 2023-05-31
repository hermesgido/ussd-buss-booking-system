from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from ussd_booking.form import *
from . models import *


def home(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

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


def trips(request):
    trips_list =enumerate(Trip.objects.all(), start=1)
    print(trips_list)
    form = TripForm()
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
           buss = form.cleaned_data['bus']
           route = form.cleaned_data['route']
           date = form.cleaned_data['date']
           
           if Trip.objects.filter(bus=buss, date=date):
               messages.error(request, "Trip with this date and buss alredy exist")
               return redirect(trips)
           if Trip.objects.filter(route=route, date=date).exists():
               messages.error(request, "Trip with this route and date alredy exist")
               return redirect(trips)
           form.save()
           messages.success(request, "Trip successfully added")
           return redirect(trips)
    
    context =  {'form': form, 'trips_list': trips_list}
    return render(request, 'trips.html', context)



def complaints(request):
    complaints_list =  enumerate(Complaint.objects.all(), start=1)
    
    context =  {'complaints': complaints_list}
    return render(request, 'complaints.html', context)
