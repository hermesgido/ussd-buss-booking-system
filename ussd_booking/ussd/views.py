import random
from datetime import datetime, timedelta
from ..models import Booking, Bus, Complaint, Passenger, Seat, Trip
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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

         #User needs a list of all buses   
        elif text == "1":
            results=enumerate(Bus.objects.all(), start=1)
            response = "CON The List of Our Busses is \n"
            for no, i in results:
                response += f"{no}. {i}\n"
            response += f"END\n"


        elif text == "2":
            response = "CON Choose an option \n"
            response += "1. Tomorrow - 23/05 \n"
            response += "2. After Tomorrow - 23/05 \n"

         #Follow up
        elif text == '2*1':
            data = f"CON Availble Roots are:[select one ] \n"
            today = datetime.today().strftime('%Y-%m-%d')
            if Trip.objects.filter(date=today).count()>0:
                trips=enumerate(Trip.objects.filter(date=today), start=1)
                for no, trip in trips:
                    data += f"{trip.id}. {trip} \n"
                response = data
            else:
                response = f"END No trip found for date: {today} \n"


        elif text == '2*2':
            print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")      
            tomorrow = datetime.today() + timedelta(days=1)
            tomorrow_date = tomorrow.strftime('%Y-%m-%d')
            data = f"CON Availble Roots are:[select one ] \n"
            if Trip.objects.filter(date=tomorrow_date).count() > 0:
                trips=enumerate(Trip.objects.filter(date=tomorrow_date), start=1)
                for no, trip in trips:
                    data += f"{trip.id}. {trip} \n"
                response = data
            else:
                response = f"END No trip found for {tomorrow_date}"
 
        
        elif  not text.endswith("OK") and not text.startswith("3") and not text.startswith("4") and not text.startswith("5"):
            trip_id = text.split('*')[-1]
            trip = Trip.objects.get(id=trip_id)
            trip = Trip.objects.get(id=trip_id)
            ticket_number = random.randint(1000, 9999)
            book = Booking.objects.create(trip = trip, user_phone = phone_number, ticket_number=ticket_number, date = datetime.today(), user_name = "Juma abdala")
            book.save()
            passenger = Passenger.objects.get_or_create(phone_number=phone_number)
            passenger.save()
            print(f"Request routed id is {trip_id}")

            response = "CON Your booking details are \n \n"
            response += f"ROUTE: {trip.route.name}\n"
            response += f"DEPARTURE PLACE: Mbezi Stand \n"
            response += f"DATE: {trip.date}\n"
            response += f"BUS NUMBER: {trip.bus.number_plate}\n"
            response += f"PRICE: {trip.route.price}\n \n"         
            response += f"Enter OK to confirm your booking \n"
            
            
        elif  text.endswith("OK"):
            print(f"Request routed id is {text}")
            if request.session.has_key('trip_id'):
               print(f"Request routed id is exists")
               trip_id = request.session['trip_id']
               if trip_id is None:
                   response = "END Trip information not found. Please start again."
               else:
                    ticket_number = random.randint(1000, 9999)
                    trip = Trip.objects.get(id=trip_id)
                    book = Booking.objects.create(trip = trip, user_phone = phone_number, date = datetime.today(), ticket_number = ticket_number, user_name = "Juma abdala")
                    book.save()
                    response = f"END Your Bokking has been successfully, You will receive a BOOKING NUMBER via SMS soon"
                
                            
            
            # seats = Seat.objects.filter(bus=route.bus)
            # if seats.count() == 0:
            #     response = "END No seats available"
            # else:
            #     response = "CON Please select a seat number:\n"
            #     available_seats = [seat.number for seat in seats if seat.is_available]
            #     response += " ".join(available_seats)  # Join the seat numbers with a space
        elif text == "3":
            ##check ticket status
            response = f"CON Enter your ticket number:"
        elif text.startswith("3*"):
            ticket_number = text.split('*')[-1]
            print(f"Enter ticket number{ticket_number}")
            if Booking.objects.filter(ticket_number=ticket_number).exists():
                booking  = Booking.objects.filter(ticket_number=ticket_number).first()
                response += f"END Your ticket Details are \n \n"
                response += f"ROUTE: {booking.trip.route.name}\n"
                response += f"DEPARTURE PLACE: Mbezi Stand \n"
                response += f"DATE: {booking.trip.date}\n"
                response += f"BUS NUMBER: {booking.trip.bus.number_plate}\n"
                response += f"PRICE: {booking.trip.route.price}\n \n"
                print(f"Enter booking it exists")           
            else:
                response = f" END No booking found with ticket number {ticket_number}."
        elif text == "4":
            ##cancel ticket
             response = f"END Please contact us to cancel your booking ticket through +255643389855"
        
        elif text == "5":
            ## report an issue
            response = "CON Write Your issues to report:"
        elif text.startswith("5*"):
            issue = text.split('*')[-1]
            us = Complaint.objects.create(message=issue, phone_number=phone_number)
            us.save()
            response = f"END Your issue have been submitted successfully, Thank you!"
        else :
            response = "Enter correct response"
        

        return HttpResponse(response)
    return HttpResponse({"message":"Feature"})