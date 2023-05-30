from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Booking)
admin.site.register(Bus)
admin.site.register(Route)

admin.site.register(Trip)
admin.site.register(Seat)