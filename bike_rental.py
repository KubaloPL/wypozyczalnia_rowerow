# IMPORTS
import json
import datetime
import smtplib
import os
from email.mime.text import MIMEText

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
    


def send_rental_invoice_email(customer_email, customer_name):
    '''
        Wysyła e-mail z fakturą.
    '''
    rental_details = rental[customer_name]
    try:
        # Configuration
        port = 587
        smtp_server = "127.0.0.1"
        login = "server_login"
        password = "server_password"

        sender_email = "email@example.com"
        receiver_email = customer_email

        # Plain text content
        text = f"""\
        Faktura:
        Osoba wynajmująca: {customer_name}
        Czas wynajmu: {rental_details["rental_duration"]} godzin
        Koszt wynajmu: {rental_details["cost"]}zł
        Data wynajmu: {datetime.date.today()}
        """
        print(text)

        # Create MIMEText object
        message = MIMEText(text, "plain")
        message["Subject"] = "Faktura za wynajem roweru"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    except Exception as error:
        print(f"BŁĄD: Wysyłanie e-maila nie powiodło się: {error}")



def generate_daily_report():
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

send_rental_invoice_email("hello@gmail.com","test")
print(rental)