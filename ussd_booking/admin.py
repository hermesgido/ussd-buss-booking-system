from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Booking)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Complaint)
admin.site.register(Schedule)
admin.site.register(Seat)
admin.site.register(Passenger) 