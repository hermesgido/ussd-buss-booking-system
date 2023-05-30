import json
from django.http import QueryDict
from typing import List, Dict

class USSDMenu:
    def PINMenu(self):
        return self.get_menu('Please enter your PIN/Password')

    def MainMenu(self):
        return self.get_menu('Welcome to the Bus Booking System\n'
                             '1. Book a Trip\n'
                             '2. Cancel a Trip\n'
                             '3. View Booked Trips\n')

    def RouteMenu(self, routes: List[str]):
        menu = self.get_menu('Select a route:\n')
        menu += self.get_menu_options(routes)
        return menu

    def BusMenu(self, buses: List[str]):
        menu = self.get_menu('Select a bus:\n')
        menu += self.get_menu_options(buses)
        return menu

    def SeatMenu(self, seats: List[str]):
        menu = self.get_menu('Select a seat:\n')
        menu += self.get_menu_options(seats)
        return menu

    def ConfirmBookingMenu(self):
        return self.get_menu('Confirm your booking:\n'
                             '1. Confirm\n'
                             '2. Cancel\n')

    def ViewBookedTripsMenu(self, trips: List[str]):
        menu = self.get_menu('Your booked trips:\n')
        menu += self.get_menu_options(trips)
        return menu

    def InvalidInputMenu(self):
        return self.get_menu('Invalid input. Please try again.')

    def get_menu(self, message: str):
        return f'CON {message}\n'

    def get_menu_options(self, options: List[str]):
        menu = ''
        for i, option in enumerate(options, start=1):
            menu += f'{i}. {option}\n'
        return menu

    def parse_text(self, text: str) -> List[str]:
        return text.strip().split('*')
