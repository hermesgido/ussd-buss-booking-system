import random
import phonenumbers
from phonenumbers.carrier import name_for_number

#this is for phone validate
class TanzaniaMNOChecker:
    def _init_(self, phone_number=None):
        self.phone_number = phone_number
        self._mno_prefixes = {
            "Vodacom": ["74", "75", "76", "77"],
            "Airtel": ["68", "69", "78", "79"],
            "Tigo": ["65", "67", "71", "77", "78", "76"],
            "Halotel": ["60", "62", "63"]
        }




    def is_valid(self, phone_number):
        try:
            parsed_number = phonenumbers.parse(str(phone_number), "TZ")
            print(parsed_number)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False

    def get_formatted_number(self):
        try:
            parsed_number = phonenumbers.parse(self.phone_number, "TZ")
            if not phonenumbers.is_valid_number(parsed_number):
                return "Invalid phone number"
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            formatted_number = formatted_number.replace(" ", "")
            return formatted_number
        except phonenumbers.phonenumberutil.NumberParseException:
            return "Invalid phone number"

    def get_mno_name(self, phone_number):
        parsed_number = phonenumbers.parse(phone_number, "TZ")
        if  self.is_valid(parsed_number):
            return "Not a correct number"
        else:
            prefix = str(parsed_number.national_number)[:2]
            for mno, prefixes in self._mno_prefixes.items():
                if prefix in prefixes:
                    return mno

    def generate_random_numbers(self, amount):
        random_numbers = []
        while len(random_numbers) < amount:
            number = "0" + str(random.randint(600000000, 799999999))
            mno = self.get_mno_name(number)
            if mno != "MNO data not available for this number" and  mno != None:
               random_numbers.append({"phone_number": number, "mno": mno})
        return random_numbers

    def get_mno(self, phone_number):
            parsed_number = phonenumbers.parse(phone_number, "TZ")
            if not phonenumbers.is_valid_number(parsed_number):
                return "Invalid phone number"
            if phonenumbers.phonenumberutil.number_type(parsed_number) != phonenumbers.PhoneNumberType.MOBILE:
                return "Not a mobile phone number"
            if phonenumbers.is_possible_number(parsed_number):
                if phonenumbers.is_valid_number_for_region(parsed_number, "TZ"):
                    if phonenumbers.region_code_for_number(parsed_number) == "TZ":
                        mno = name_for_number(parsed_number, "en")
                        if mno:
                            if mno == "tiGO":
                                return "Tigo"
                            if mno == "Zantel":
                                return "Tigo"
                            elif mno == "Vodacom":
                                return "Vodacom"
                            elif mno == "Viettel":
                                return "Halotel"
                            elif mno == "Tanzania Telecom":
                                return "TTCL"
                            else:
                                pass
                            return "MNO data not available for this number"
                    else:
                        return "Phone number is not from Tanzania"
                else:
                    return "Phone number is not possible"
            else:
                return "Phone number is not valid"
            
            
def get_mnoz():
    parsed_number = phonenumbers.parse("255777856102", "TZ")
    if not phonenumbers.is_valid_number(parsed_number):
        return "Invalid phone number"
    if phonenumbers.phonenumberutil.number_type(parsed_number) != phonenumbers.PhoneNumberType.MOBILE:
        return "Not a mobile phone number"
    if phonenumbers.is_possible_number(parsed_number):
        if phonenumbers.is_valid_number_for_region(parsed_number, "TZ"):
            if phonenumbers.region_code_for_number(parsed_number) == "TZ":
                mno = name_for_number(parsed_number, "en")
                print( mno)
get_mnoz()