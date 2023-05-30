from django.db import models
from django.contrib.auth.models import User


class Route(models.Model):
    name = models.CharField(max_length=100)
    departure_point = models.CharField(max_length=100)
    arrival_point = models.CharField(max_length=100)
    distance = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Bus(models.Model):
    number_plate = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()
    model = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.number_plate
class Trip(models.Model):
    route = models.ForeignKey(Route, null=True, blank=True, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return self.route.name + " " + str(self.date)

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.number

class Booking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True)
    user_phone = models.CharField(max_length=120, null=True, blank=True)
    user_name = models.CharField(max_length=200, null=True)
    ticket_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.trip} - {self.seat}"

class Complaint(models.Model):
    phone_number =  models.CharField(max_length=20)
    message = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True)
    