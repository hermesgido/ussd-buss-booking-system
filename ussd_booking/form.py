# forms.py
from django import forms
from .models import *

class MainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                widget_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                widget_class = 'form-control form-small select'
            elif isinstance(field.widget, forms.Textarea) and isinstance(field, forms.CharField):
                field.widget.attrs['rows'] = 1
                field.widget.attrs['cols'] = 1
            field.widget.attrs['class'] = widget_class
            
            
class UserRegistrationForm(forms.Form):
    ROLES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
    )

    full_name = forms.CharField(
        label='Full Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        label='Role',
        choices=ROLES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class BussForm(MainForm):
    class Meta:

        model = Bus
        exclude =['id']
class RouteForm(MainForm):
    class Meta:

        model = Route
        exclude =['id']


class BookingForm(MainForm):
    class Meta:
        model = Booking
        exclude =['id']
        

class ScheduleForm(MainForm):

    class Meta:

        model = Schedule
        exclude =['id']
        
class ComplaintForm(MainForm):
    class Meta:
        models = Complaint
        exclude =['id']
