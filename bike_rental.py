# IMPORTS
import json
import datetime
import smtplib
import os
import re
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
    now = datetime.datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    rental[customer_name] = {"rental_duration": rental_duration, "cost": cost, "rental_time": time}

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

def email_validator(email):    
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return EMAIL_REGEX.match(email)

# MAIN FUNCTION



def main():
    print("Opcja 1: Wyświetl wszystkie wynajmy")
    print("Opcja 2: Dodawanie wynajmu")
    print("Opcja 3: Anulowanie wynajmu")
    print("Opcja 4: Generowanie dziennego raportu")
    print("Opcja 5: Wysyłanie E-maila z fakturą")
    print("Opcja 6: Wyjście z programu")
    option = input("Wybierz opcje: ")

    if option == "1": #printing out rentals
        print(rental)



    elif option == "2": #adding rental
        customer_name = input("Podaj nazwę użytkownika dla którego chcesz dodać wynajem: ")
        rental_duration = input("Podaj ilość godzin wynajmu: ")
        if not rental_duration.isnumeric():
            print("BŁĄD: podana wartość nie jest liczbą.")
            return
        rental_duration = int(rental_duration)
        if rental_duration == 0:
            print("BŁĄD: nie można wynająć roweru na 0 godzin.")
            return
        rent_bike(customer_name, rental_duration)
        print(f"Pomyślnie dodano wynajem wynajem dla {customer_name} o długości {rental_duration}h w cenie {calculate_cost(rental_duration)}zł")


    elif option == "3": #cancelling rental
        customer_name = input("Podaj nazwę użytkownika dla którego chcesz anulować wynajem: ")
        if not customer_name in rental:
            print("BŁĄD: Ten użytkownik nie posiada żadnego wynajmu.")
            return
    
        cancel_rental(customer_name)
        print(f"Pomyślnie anulowano wynajem dla {customer_name}")



    elif option == "4": #generating daily report
        generate_daily_report()
        print(f"Pomyślnie wygenerowano dzisiejszy raport. Zapisano do pliku 'data/daily_report_{datetime.date.today()}.json'")



    elif option == "5": #sending email
        customer_email = input("Podaj E-Mail dla którego chcesz wysłać fakturę: ")
        if email_validator(customer_email) == None:
            print("BŁĄD: Nieprawidłowy E-Mail")
            return
        customer_name = input("Podaj nazwę użytkownika którego wynajem chcesz wysłać: ")

        if not customer_name in rental:
            print("BŁĄD: Ten użytkownik nie posiada żadnego wynajmu.")
            return

        send_rental_invoice_email(customer_email, customer_name)

        print(f"Pomyślnie wysłano email")



    elif option == "6": #exiting the program
            return "end"
        


    else: #invalid option
            print("BŁĄD: Nie znaleziono takiej opcji")

load_rentals()

while True:
    if main() == "end":
        break
    else:
        input("\nNaciśnij enter aby kontynuować...\n")

#TODO google calendar integration