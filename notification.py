import smtplib
import ssl
import logging
from os import getenv
from email.message import EmailMessage
from dotenv import load_dotenv
from subscriber import Subscriber


class Notification:
    """Represents an email content, that will be sent to the Subsciber"""

    def __init__(self, scrapped_data: dict):
        self.scrapping_data = scrapped_data
        self.notification = self.create()

    def create(self):
        """
        Creates a notification that will be sent by email.

        Returns:
            str: the content of the notification
        """
        h, m, s = self.scrapping_data["time_to_flight"]
        self.notification = f'Przelot ISS dnia {self.scrapping_data["flight_date_pl"]} w {self.scrapping_data["city"]}:\n' \
                            f'\n' \
                            f'{self.scrapping_data["name_start"]}: {self.scrapping_data["time_start"]}\n' \
                            f'{self.scrapping_data["name_end"]}: {self.scrapping_data["time_end"]}\n' \
                            f'{self.scrapping_data["flight_duration"]}\n' \
                            f'Do przelotu pozostało: {h}h {m}m {round(float(s))}s\n' \
                            f'{self.scrapping_data["brightness"]}\n' \
                            f'Max wysokość nad horyzontem:{self.scrapping_data["max_altitude"]}'

        logging.info(self.notification)

        return self.notification

    def send_mail_to(self, subscriber: Subscriber):
        """
        Sends an email with the notification to the subsciber.

        Args:
            subscriber (Subscriber): the person who will receive the notification
        """
        load_dotenv()
        smtp_port = int(getenv("SMTP_PORT"))
        smtp_server = getenv("SMTP_SERVER")
        sender_email = getenv("EMAIL")
        sender_password = getenv("PASSWORD")

        message = EmailMessage()
        message['From'] = getenv("EMAIL")
        message['To'] = subscriber.email
        message['Subject'] = f'Przelot ISS dnia {self.scrapping_data["flight_date_pl"]} w {self.scrapping_data["city"]}'
        message.set_content(self.notification)
        message.set_charset('utf-8')

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
            logging.info('Wiadomosc (powiadomienie) wyslano poprawnie.')
