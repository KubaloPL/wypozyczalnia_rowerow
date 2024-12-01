import json
import datetime
import smtplib
import os

rental = {}

RENTALS_PATH = "data/rentals.json"

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

def load_rentals(): #TODO
    '''
        Wczytuje wynajmy z pliku JSON.
    '''

def cancel_rental(customer_name): #TODO
    '''
        Usuwa wynajem.
    '''
    
def send_rental_invoice_email(customer_email, rental_details): #TODO
    '''
        Wysyła e-mail z fakturą.
    '''


def sgenerate_daily_report(): #TODO
    '''
        Generuje raport dzienny.
    '''


rent_bike("test", 10)

print(rental)