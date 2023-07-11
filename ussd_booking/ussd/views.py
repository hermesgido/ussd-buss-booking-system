from __future__ import print_function
import random
from datetime import datetime, timedelta
from ..models import Booking, Bus, Complaint, Passenger, Route, Seat, Schedule
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import africastalking
from django.core.cache import cache
import os
import dotenv
dotenv.load_dotenv()

class BusSeats:
    def __init__(self, seats):
        self.seats = seats

    def filter_available_seats(self, sold_seats):
        num_columns = 4
        available_seats = self.seats[:]  # Create a copy of seats to avoid modifying the original list

        # Update specific index elements with "xx"
        for seat in sold_seats:
            if seat < len(available_seats):
                available_seats[seat] = "xx"

        # Format seats with four columns and add spacing between the second and third columns
        formatted_rows = []
        for i in range(0, len(available_seats), num_columns):
            row = available_seats[i:i+num_columns]
            if i == 0:  # Only for the first row
                formatted_row = '______' +' '+ ' '*3 + row[0] + ' ' + row[1]
            else:
                formatted_row = row[0] + ' ' + row[1] + '    ' + row[2] + ' ' + row[3] if len(row) == 4 else ' '.join(row)
            formatted_rows.append(formatted_row)

        formatted_string = '\n'.join(formatted_rows)
        return formatted_string


# # Example usage
# bus_seats = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
# bus = BusSeats(bus_seats)
# sold_seats = [2, 4, 7]
# result = bus.filter_available_seats(sold_seats)
# print(result)


def send_sms_api(phone_number, message):
    # Set your app credentials
    username = os.getenv('SANDBOX_USER')
    api_key = os.getenv('DEV_API_KEY')
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS
    recipients = phone_number
    message = message
    sender = "NEW FORCE"
    try:
        # Thats it, hit send and we'll take care of the rest.
        response = africastalking.SMS.send(message, recipients, sender)
        print(response)
    except Exception as e:
        print('Encountered an error while sending: %s' % str(e))


@csrf_exempt
def ussd_callback2(request):
    def go_Back(text):
        textArray = text.split("*")
        while "98" in textArray:
            # Find the index of the next occurrence of the "go back" token.
            startIndex = textArray.index("98")
            # Remove the two textArray at the index of the "go back" token.
            textArray.pop(startIndex)
            textArray.pop(startIndex - 1)
        # Join the textArray back together into a string.
        return ("*".join(textArray))

    def goToMainMenu(text):
        explodedText = text.split("*")
        while "99" in explodedText:
            firstIndex = explodedText.index("99")
            explodedText = explodedText[firstIndex + 1:]
        return ("*".join(explodedText))

    if request.method == 'POST':
        print(datetime.today())
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        text = go_Back(goToMainMenu(text))
        response = ""
        print(f"the entered text iss {text}")
        if text == "":
            response = "CON Welcome to New Force bus Booking ! \n Which service would you like to access? \n"
            response += "1. List all our buses \n"
            response += "2. Book a Trip \n"
            response += "3. Check ticket status \n"
            response += "4. Cancel a booking \n"
            response += "5. Report an issue"

        elif text == "1":
            results = enumerate(Bus.objects.all(), start=1)
            response = "CON The List of Our Busses: \n"

            for no, i in results:
                response += f"=> {i}\n"
            response += "98. Go Back \n 99. Main Menu"

        elif text == "2":
            response = "CON Choose an route \n"
            response += f"1.DAR-MORO \n 2. DAR-MBEYA \n 3. DAR-SONGEA \n 4. DAR-SUMBAWANGA \n"
            response += "98. Go Back \n 99. Main Menu"
        elif text == "2*1" or text == "2*2" or text == "2*3" or text == "2*4":
            cache.set('route_name', "DAR-MORO") if text == "2*1" else cache.set('route_name', "DAR-MBEYA") if text == "2*2" else cache.set(
                'route_name', "DAR-SONGEA") if text == "2*3" else cache.set('route_name', "DAR-SUMBAWANGA") if text == "2*4" else "0"
            route_name_cached = cache.get('route_name')
            print(route_name_cached)
            response = "CON Choose an option \n"
            response += f"1. Tomorrow - {(datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')} \n"
            response += f"2. After Tomorrow - {(datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')} \n"
            response += "98. Go Back \n 99. Main Menu"

        elif text == "2*1*1" or text == "2*2*1" or text == "2*3*1" or text == "2*4*1":
            cache.set("trip_date", 1)
            route_name_cached = cache.get('route_name')
            if Schedule.objects.filter(route__name=route_name_cached, date=datetime.today() + timedelta(days=1)).exists():
                schedule = Schedule.objects.get(
                    route__name=route_name_cached, date=datetime.today() + timedelta(days=1))
                bookings = Booking.objects.filter(schedule=schedule)
                booked_seats = [int(booking.seat_number)
                                for booking in bookings]
                # seats_per_row = 4  # Number of seats per row
                # total_seats = 30  # Total number of seats
                # response = "CON Please select a seat number:\n"

                # for i in range(total_seats):
                #     # Pad seat number with leading zeros
                #     seat_number = str(i + 1).zfill(2)
                #     # Check if the seat is booked
                #     if i + 1 in booked_seats:
                #         seat_number = "XX"
                #     if i % seats_per_row == 0 and i > 0:
                #         response += "\n"  # Add a new line after each row
                #     response += seat_number + " "
                    
                bus_seats = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
                bus = BusSeats(bus_seats)
                sold_seats = [(booking.seat_number) for booking in bookings]
                result = bus.filter_available_seats(sold_seats)
                
                response = "CON Please select a seat number:\n"
                response += str(result)
                response += "\n 98. Go Back \n 99. Main Menu"
            else:
                response = "CON No Trip Found\n"
                response += "98. Go Back \n 99. Main Menu"

        elif text.startswith("2*1*1*") or text.startswith("2*1*2*") or text.startswith("2*1*3*") or text.startswith("2*1*4*") or text.startswith("2*2*1*") or text.startswith("2*2*2*") or text.startswith("2*2*3*") or text.startswith("2*2*4*"):
            seat_number = text.split("*")[-1]
            print(seat_number)
            cache.set("seat_number", seat_number)
            seat_number = cache.get("seat_number")
            trip_date = cache.get("trip_date")
            route_name_cached = cache.get('route_name')
            print(trip_date, route_name_cached)

            trip_date_new = datetime.today() + timedelta(days=1) if trip_date == 1 else datetime.today() + \
                timedelta(days=2) if trip_date == 2 else None
            if trip_date_new is None:
                print("Noneeeeeeeeeeeeeeeeeeeeee")
            else:
                print(f"not noneeeeeeeeeee {trip_date_new}")

            schedule = Schedule.objects.filter(route=Route.objects.filter(
                name=route_name_cached).first(), date=trip_date_new).first()
            print(Booking.objects.filter(
                seat_number=seat_number,  schedule=schedule).exists())
            if Booking.objects.filter(seat_number=seat_number, schedule=schedule).exists():
                response = "CON This Seat Is Already booked \n"
                response += "98. Go Back \n 99. Main Menu"

            else:
                schedule = Schedule.objects.filter(route=Route.objects.filter(
                    name=route_name_cached).first(), date=trip_date_new).first()
                ticket_number = random.randint(1000, 9999)
                book = Booking.objects.create(seat_number=seat_number, ticket_number=ticket_number,
                                              schedule=schedule, date=trip_date_new, user_phone=phone_number, user_name="Joseph Michael")
                book.save()
                passenger, create = Passenger.objects.get_or_create(
                    phone_number=phone_number)
                passenger.save()
                message = f"Your Booking is successful, Ticket number is {ticket_number}"
                # send_sms_api(phone_number = [str(phone_number)], message = message)
                response = f"CON Your booking details are \n \n"
                response += f"ROUTE: {schedule.route.name}\n"
                response += f"SEAT NO: {book.seat_number}\n"
                response += f"DEPARTURE PLACE: Mbezi Stand \n"
                response += f"DATE: {schedule.date}\n"
                response += f"BUS NUMBER: {schedule.bus.number_plate}\n"
                response += f"PRICE: {schedule.route.price}\n \n"
                response += f"Ticket number is {ticket_number}\n"
                response += "98. Go Back \n 99. Main Menu \n"
                response += f"Check Your SMS inbox for more details \n"

        elif text == "2*1*2" or text == "2*2*2" or text == "2*3*2" or text == "2*4*2" and not text.endswith("99"):
            cache.set("trip_date", 2)
            route_name_cached = cache.get('route_name')
            if Schedule.objects.filter(route__name=route_name_cached, date=datetime.today() + timedelta(days=2)).exists():
                schedule = Schedule.objects.get(
                    route__name=route_name_cached, date=datetime.today() + timedelta(days=2))
                bookings = Booking.objects.filter(schedule=schedule)
                booked_seats = [int(booking.seat_number) for booking in bookings]
                # seats_per_row = 4  # Number of seats per row
                # total_seats = 30  # Total number of seats
                # response = "CON Please select a seat number:\n"
                # for i in range(total_seats):
                #     # Pad seat number with leading zeros
                #     seat_number = str(i + 1).zfill(2)
                #     # Check if the seat is booked
                #     if i + 1 in booked_seats:
                #         seat_number = "XX"
                #     if i % seats_per_row == 0 and i > 0:
                #         response += "\n"  # Add a new line after each row
                #     response += seat_number + " "
                
                bus_seats = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
                bus = BusSeats(bus_seats)
                sold_seats = [str(booking.seat_number) for booking in bookings]
                result = bus.filter_available_seats(sold_seats)
                
                response += "98. Go Back \n 99. Main Menu"

            else:
                response = "CON No Trip Found\n"
                response += "98. Go Back \n 99. Main Menu"

        elif text == "3":
            # check ticket status
            response = f"CON Enter your ticket number: \n"
            response += "98. Go Back \n 99. Main Menu"

        elif text.startswith("3*"):
            ticket_number = text.split('*')[-1]
            print(f"Enter ticket number{ticket_number}")
            if Booking.objects.filter(ticket_number=ticket_number).exists():
                booking = Booking.objects.filter(ticket_number=ticket_number).first()
                response += f"CON Your ticket Details are \n \n"
                response += f"ROUTE: {booking.schedule.route.name}\n"
                response += f"DEPARTURE PLACE: Mbezi Stand \n"
                response += f"DATE: {booking.schedule.date}\n"
                response += f"BUS NUMBER: {booking.schedule.bus.number_plate}\n"
                response += f"PRICE: {booking.schedule.route.price}\n"
                response += "98. Go Back \n 99. Main Menu"

                print(f"Enter booking it exists")
            else:
                response = f"CON No booking found with ticket number {ticket_number}.\n"
                response += "98. Go Back \n 99. Main Menu"

        elif text == "4":
            # cancel ticket
            response = f"CON Please contact us to cancel your booking ticket through +255643389855 \n"
            response += "98. Go Back \n 99. Main Menu"

        elif text == "5":
            # report an issue
            response = "CON Write Your issues to report:\n"
            response += "98. Go Back \n 99. Main Menu"

        elif text.startswith("5*"):
            issue = text.split('*')[-1]
            us = Complaint.objects.create(
                message=issue, phone_number=phone_number)
            us.save()
            response = f"CON Your issue have been submitted successfully, Thank you!\n"
            response += "98. Go Back \n 99. Main Menu"

        elif text.endswith("99"):
            response = "CON Your Booking is successfully completed: Please check your booking ticket via sms \n"
            response += "98. Go Back \n 99. Main Menu"
        else:
            response = "Enter correct response"
        return HttpResponse(response)
    return HttpResponse({"message": "Feature"})


# Create your views here.
@csrf_exempt
def ussd_callback(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""
        print(f"the entered text iss {text}")

        if text == "":
            response = "CON Welcome! \n Which service would you like to access? \n"
            response += "1. List all our buses \n"
            response += "2. Book a Trip \n"
            response += "3. Check ticket status \n"
            response += "4. Cancel a booking \n"
            response += "5. Report an issue"

         # User needs a list of all buses
        elif text == "1":
            results = enumerate(Bus.objects.all(), start=1)
            response = "CON The List of Our Busses is \n"
            for no, i in results:
                response += f"{no}. {i}\n"
            response += "98. Go Back \n 99. Main Menu"

        elif text == "2":
            response = "CON Choose an option \n"
            response += f"1. Tomorrow - {(datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')} \n"
            response += f"2. After Tomorrow - {(datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')} \n"
            response += "98. Go Back \n 99. Main Menu"

         # Follow up
        elif text == '2*1':
            data = f"CON Availble Roots are:[select one ] \n"
            today = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
            if Schedule.objects.filter(date=today).count() > 0:
                schedule = enumerate(
                    Schedule.objects.filter(date=today), start=1)
                for no, schedule in schedule:
                    data += f"{schedule.id}. {schedule} \n"
                response = data
            else:
                response = f"CON No trip found for date: {today} \n"
                response += "98. Go Back \n 99. Main Menu"

        elif text == '2*2':
            print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
            tomorrow = datetime.today() + timedelta(days=2)
            tomorrow_date = tomorrow.strftime('%Y-%m-%d')
            data = f"CON Availble Roots are:[select one ] \n"
            if Schedule.objects.filter(date=tomorrow_date).count() > 0:
                schedule = enumerate(Schedule.objects.filter(
                    date=tomorrow_date), start=1)
                for no, schedule in schedule:
                    data += f"{schedule.id}. {schedule} \n"
                response = data
                response += "\n98. Go Back \n 99. Main Menu"

            else:
                response = f"END No trip found for {tomorrow_date}\n"
                response += "98. Go Back \n 99. Main Menu"

        elif not text.endswith("OK") and not text.startswith("3") and not text.startswith("4") and not text.startswith("5"):
            schedule_id = text.split('*')[-1]
            schedule = Schedule.objects.get(id=schedule_id)
            schedule = Schedule.objects.get(id=schedule_id)
            ticket_number = random.randint(1000, 9999)
            book = Booking.objects.create(schedule=schedule, user_phone=phone_number,
                                          ticket_number=ticket_number, date=datetime.today(), user_name="Joseph Michael")
            book.save()
            passenger, create = Passenger.objects.get_or_create(
                phone_number=phone_number)
            passenger.save()
            message = f"Your Booking is successful, Ticket number is {ticket_number}"
            send_sms_api(phone_number=[str(phone_number)], message=message)
            print(f"Request routed id is {schedule_id}")

            response = "CON Your booking details are \n \n"
            response += f"ROUTE: {schedule.route.name}\n"
            response += f"DEPARTURE PLACE: Mbezi Stand \n"
            response += f"DATE: {schedule.date}\n"
            response += f"BUS NUMBER: {schedule.bus.number_plate}\n"
            response += f"PRICE: {schedule.route.price}\n \n"
            response += f"Enter OK to confirm your booking \n"
            response += "98. Go Back \n 99. Main Menu"

            # seats = Seat.objects.filter(bus=route.bus)
            # if seats.count() == 0:
            #     response = "END No seats available"
            # else:
            #     response = "CON Please select a seat number:\n"
            #     available_seats = [seat.number for seat in seats if seat.is_available]
            #     response += " ".join(available_seats)  # Join the seat numbers with a space
        elif text == "3":
            # check ticket status
            response = f"CON Enter your ticket number: \n"
            response += "98. Go Back \n 99. Main Menu"
        elif text.startswith("3*"):
            ticket_number = text.split('*')[-1]
            print(f"Enter ticket number{ticket_number}")
            if Booking.objects.filter(ticket_number=ticket_number).exists():
                booking = Booking.objects.filter(
                    ticket_number=ticket_number).first()
                response += f"END Your ticket Details are \n \n"
                response += f"ROUTE: {booking.schedule.route.name}\n"
                response += f"DEPARTURE PLACE: Mbezi Stand \n"
                response += f"DATE: {booking.schedule.date}\n"
                response += f"BUS NUMBER: {booking.schedule.bus.number_plate}\n"
                response += f"PRICE: {booking.schedule.route.price}\n \n"
                response += "98. Go Back \n 99. Main Menu"
                print(f"Enter booking it exists")
            else:
                response = f" CON No booking found with ticket number {ticket_number}.\n"
                response += "98. Go Back \n 99. Main Menu"
        elif text == "4":
            # cancel ticket
            response = f"CON Please contact us to cancel your booking ticket through +255643389855 \n"
            response += "98. Go Back \n 99. Main Menu"
        elif text == "5":
            # report an issue
            response = "CON Write Your issues to report: \n"
            response += "98. Go Back \n 99. Main Menu"
        elif text.startswith("5*"):
            issue = text.split('*')[-1]
            us = Complaint.objects.create(
                message=issue, phone_number=phone_number)
            us.save()
            response = f"CON Your issue have been submitted successfully, Thank you! \n"
            response += "98. Go Back \n 99. Main Menu"
        else:
            response = "Enter correct response"

        return HttpResponse(response)
    return HttpResponse({"message": "Feature"})
