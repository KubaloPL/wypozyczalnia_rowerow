# IMPORTS
import json
import datetime
import smtplib
import os

# CONFIGURABLE GLOBALS
DATA_PATH = f"data"
RENTALS_PATH = f"{DATA_PATH}/rentals.json"

# VARIABLES
rental = {}

# FUNCTIONS

def rent_bike(customer_name, rental_duration):
    '''
        Dodaje wynajem roweru
    '''
    cost = calculate_cost(rental_duration)
    rental[customer_name] = {"rental_duration": rental_duration, "cost": cost}

    save_rental(rental)

def calculate_cost(rental_duration: int) -> int:
    '''
        Oblicza koszt wynajmu
        Calculates the cost of a rental from duration in hours

        returns cost of rental in zł
    '''
    cost = 10 + (rental_duration - 1) * 5
    return cost



def save_rental(rental):
    '''
        Zapisuje dane wynajmu do pliku JSON.
    '''
    if not os.path.exists(RENTALS_PATH):
        open(RENTALS_PATH,"x")

    file = open(RENTALS_PATH,"w")
    json.dump(rental, file)
    file.close()



def load_rentals():
    '''
        Wczytuje wynajmy z pliku JSON.
    '''
    file = open(RENTALS_PATH, "r")
    rental = json.load(file)
    print(f"loading rentals from json: {rental}")



def cancel_rental(customer_name):
    '''
        Usuwa wynajem.
    '''
    load_rentals()
    rental.pop(customer_name, None)
    save_rental(rental)
    


def send_rental_invoice_email(customer_email, rental_details): #TODO
    '''
        Wysyła e-mail z fakturą.
    '''


def generate_daily_report(): #TODO
    '''
        Generuje raport dzienny.
    '''
    path = f"data/daily_report_{datetime.date.today()}.json"
    file = open(path, "w")
    json.dump(rental, file)
    file.close()

# MAIN FUNCTION


load_rentals()
rent_bike("test", 10)

generate_daily_report()

print(rental)