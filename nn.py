# bus_booking/views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# bus_booking/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Route, Bus, Seat

class USSDCallbackView(APIView):
    def post(self, request, format=None):
        session_id = request.data.get('sessionId', '')
        service_code = request.data.get('serviceCode', '')
        phone_number = request.data.get('phoneNumber', '')
        text = request.data.get('text', '')

        response = ""

        # Example: Welcome message
 # bus_booking/views.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# bus_booking/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Route, Bus, Seat

class USSDCallbackView(APIView):
    def post(self, request, format=None):
        session_id = request.data.get('sessionId', '')
        service_code = request.data.get('serviceCode', '')
        phone_number = request.data.get('phoneNumber', '')
        text = request.data.get('text', '')

        response = ""

        # Example: Welcome message
        if text == "":
            response = "CON Welcome to the Bus Booking System. \n"
            response += "1. Book a Trip \n"
            response += "2. Cancel a Trip \n"
            response += "3. View Booked Trips"

        # Example: Handle book a trip
        elif text == "1":
            # Get the available routes
            routes = Route.objects.all()

            # Generate the response with the list of routes
            response = "CON Select a route: \n"
            for i, route in enumerate(routes, start=1):
                response += f"{i}. {route}\n"

        # Example: Handle route selection
        elif text.startswith("1*"):
            route_index = int(text.split("*")[1])
            routes = Route.objects.all()

            if 1 <= route_index <= len(routes):
                selected_route = routes[route_index - 1]

                # Get the available buses for the selected route
                buses = Bus.objects.filter(route=selected_route)

                # Generate the response with the list of buses
                response = "CON Select a bus: \n"
                for i, bus in enumerate(buses, start=1):
                    response += f"{i}. {bus}\n"

        # Example: Handle bus selection
        elif text.startswith("1*route_index*"):
            route_index, bus_index = map(int, text.split("*")[1:3])
            routes = Route.objects.all()
            buses = Bus.objects.filter(route=routes[route_index - 1])

            if 1 <= bus_index <= len(buses):
                selected_bus = buses[bus_index - 1]

                # Get the available seats for the selected bus
                seats = Seat.objects.filter(bus=selected_bus, is_available=True)

                # Generate the response with the list of seats
                response = "CON Select a seat: \n"
                for seat in seats:
                    response += f"{seat}\n"

        # Example: Handle seat selection and confirmation
        elif text.startswith("1*route_index*bus_index*"):
            route_index, bus_index, seat_index = map(int, text.split("*")[1:4])
            routes = Route.objects.all()
            buses = Bus.objects.filter(route=routes[route_index - 1])

            if 1 <= bus_index <= len(buses):
                selected_bus = buses[bus_index - 1]

                seats = Seat.objects.filter(bus=selected_bus, is_available=True)

                if 1 <= seat_index <= len(seats):
                    selected_seat = seats[seat_index - 1]

                    # Perform the booking logic and confirm the booking
                    booking_successful = True

                    if booking_successful:
                        response = "END Booking confirmed. Seat booked: " + str(selected_seat)
                    else:
                        response = "END Booking failed. Please try again."

        # Example: Cancel a trip
        elif text == "2":
            # Handle cancellation logic
            response = "END Trip cancellation feature is not available yet."
        # Example: View booked trips
        elif text == "3":
            # Handle viewing booked trips logic
            # Retrieve the user's booked trips from the database
            user = request.user
            booked_trips = Booking.objects.filter(user=user)

            if booked_trips.exists():
                response = "CON Your booked trips: \n"
                for trip in booked_trips:
                    response += f"{trip}\n"
            else:
                response = "END You have no booked trips."

        # Example: Invalid input
        else:
            response = "CON Invalid input. Please try again."

        return Response(response, content_type='text/plain')



        # Example: Handle book a trip
        elif text == "1":
            # Get the available routes
            routes = Route.objects.all()

            # Generate the response with the list of routes
            response = "CON Select a route: \n"
            for i, route in enumerate(routes, start=1):
                response += f"{i}. {route}\n"

        # Example: Handle route selection
        elif text.startswith("1*"):
            route_index = int(text.split("*")[1])
            routes = Route.objects.all()

            if 1 <= route_index <= len(routes):
                selected_route = routes[route_index - 1]

                # Get the available buses for the selected route
                buses = Bus.objects.filter(route=selected_route)

                # Generate the response with the list of buses
                response = "CON Select a bus: \n"
                for i, bus in enumerate(buses, start=1):
                    response += f"{i}. {bus}\n"

        # Example: Handle bus selection
        elif text.startswith("1*route_index*"):
            route_index, bus_index = map(int, text.split("*")[1:3])
            routes = Route.objects.all()
            buses = Bus.objects.filter(route=routes[route_index - 1])

            if 1 <= bus_index <= len(buses):
                selected_bus = buses[bus_index - 1]

                # Get the available seats for the selected bus
                seats = Seat.objects.filter(bus=selected_bus, is_available=True)

                # Generate the response with the list of seats
                response = "CON Select a seat: \n"
                for seat in seats:
                    response += f"{seat}\n"

        # Example: Handle seat selection and confirmation
        elif text.startswith("1*route_index*bus_index*"):
            route_index, bus_index, seat_index = map(int, text.split("*")[1:4])
            routes = Route.objects.all()
            buses = Bus.objects.filter(route=routes[route_index - 1])

            if 1 <= bus_index <= len(buses):
                selected_bus = buses[bus_index - 1]

                seats = Seat.objects.filter(bus=selected_bus, is_available=True)

                if 1 <= seat_index <= len(seats):
                    selected_seat = seats[seat_index - 1]

                    # Perform the booking logic and confirm the booking
                    booking_successful = True

                    if booking_successful:
                        response = "END Booking confirmed. Seat booked: " + str(selected_seat)
                    else:
                        response = "END Booking failed. Please try again."

        # Example: Cancel a trip
        elif text == "2":
            # Handle cancellation logic
            response = "END Trip cancellation feature is not available yet."
        # Example: View booked trips
        elif text == "3":
            # Handle viewing booked trips logic
            # Retrieve the user's booked trips from the database
            user = request.user
            booked_trips = Booking.objects.filter(user=user)

            if booked_trips.exists():
                response = "CON Your booked trips: \n"
                for trip in booked_trips:
                    response += f"{trip}\n"
            else:
                response = "END You have no booked trips."

        # Example: Invalid input
        else:
            response = "CON Invalid input. Please try again."

        return Response(response, content_type='text/plain')

