import smtplib
import ssl
import logging
from os import getenv
from email.message import EmailMessage
from dotenv import load_dotenv
from subscriber import Subscriber


class Notification:
    """Represents an email content, that will be sent to the Subsciber"""

    def __init__(self, flyby_data: dict) -> None:
        self.flyby_data = flyby_data
        self.notification = self.create()

    def create(self) -> str:
        """
        Creates a notification that will be sent by email.

        Returns:
            str: the content of the notification
        """

        self.notification = f'Początek przelotu: {self.flyby_data["flyby_start_time"]}\n' \
                            f'Koniec przelotu: {self.flyby_data["flyby_end_time"]}\n' \
                            f'Długość przelotu: {self.flyby_data["flyby_duration"]}\n' \
                            f'Jasność w najwyższym punkcie: {self.flyby_data["flyby_brightness"]}\n' \
                            f'Max wysokość nad horyzontem: {self.flyby_data["flyby_max_altitude"]}'

        logging.info(self.notification)

        return self.notification

    def send_mail_to(self, subscriber: Subscriber) -> None:
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
        message['Subject'] = f'Przelot satelity'
        message.set_content(self.notification)
        message.set_charset('utf-8')

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
            logging.info('Wiadomość (powiadomienie) została wysłana poprawnie.')
