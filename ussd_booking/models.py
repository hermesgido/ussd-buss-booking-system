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
class Schedule(models.Model):
    route = models.ForeignKey(Route, null=True, blank=True, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()
    departure_time = models.TimeField(null=True)
    
    def __str__(self):
        return self.route.name + " " + str(self.date)

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.number

class Booking(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    #seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True)
    sit = ((1, 1), (2, 2), (3, 3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12), (13,13), (14,14), (15,15), (16,16), (17,17),(18,18), (19,19), (20,20),(21,21), (22,22), (23,23), (24,24), (25,25), (26,26),(27,27), (28,28), (29,29),(30,30))
    seat_number = models.PositiveIntegerField(null=True, choices=sit)
    date = models.DateTimeField(auto_now=True, null=True)
    user_phone = models.CharField(max_length=120, null=True, blank=True)
    user_name = models.CharField(max_length=200, null=True)
    ticket_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.schedule} - {self.seat_number}"

class Complaint(models.Model):
    phone_number =  models.CharField(max_length=20)
    message = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True)

class Passenger(models.Model):
    phone_number  = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    choice = (("Male", "Male"), ("Female", "Female"))
    gender = models.CharField(max_length=100, choices=choice, null=True, blank=True)