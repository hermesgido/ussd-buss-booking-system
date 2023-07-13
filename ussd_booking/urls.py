from django.urls import path
from  .ussd.views import ussd_callback, ussd_callback2
from . import views

urlpatterns = [
    path('ussd_callback/', ussd_callback, name='ussd_callback'),
    path('ussd_callback2/', ussd_callback2, name='ussd_callback2'),


    path('', views.login_view, name="login"),
    path('index/', views.home, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('users/', views.users, name="users"),
    path('busses/', views.busses, name="busses"),
    path('bookings/', views.bookings, name="bookings"),
    path('routes/', views.routes, name="routes"),
    path('schedule/', views.schedule, name="schedule"),
    path('complaints/', views.complaints, name="complaints"),
    
    path("delete_schedule/<str:id>/", views.delete_schedule, name="delete_schedule"),
    path("delete_user/<str:id>/", views.delete_user, name="delete_user"),

]
