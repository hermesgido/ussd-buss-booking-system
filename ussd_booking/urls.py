from django.urls import path
from  .ussd.views import ussd_callback
from . import views

urlpatterns = [
    path('ussd_callback/', ussd_callback, name='ussd_callback'),
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('users/', views.users, name="users"),
    path('busses/', views.busses, name="busses"),
    path('bookings/', views.bookings, name="bookings"),
    path('routes/', views.routes, name="routes"),
    path('trips/', views.trips, name="trips"),
    path('complaints/', views.complaints, name="complaints"),
     
]
