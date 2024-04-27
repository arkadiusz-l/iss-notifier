import logging
import smtplib
import ssl
from email.message import EmailMessage
from os import getenv
from dotenv import load_dotenv
from subscriber import Subscriber


class Notification:
    """Represents an email content, that will be sent to the Subsciber"""

    def __init__(self, flyby_data: dict) -> None:
        self.flyby_data = flyby_data
        self.content = self.create()

    def create(self) -> str:
        """
        Creates a notification that will be sent by email.

        Returns:
            str: the content of the notification
        """

        self.content = f'Początek widoczności: {self.flyby_data["start_time"]}, wysokość: {self.flyby_data["start_altitude"]}\n' \
                       f'Koniec widoczności: {self.flyby_data["end_time"]}, wysokość: {self.flyby_data["end_altitude"]}\n' \
                       f'Długość przelotu: {self.flyby_data["duration"]}\n' \
                       f'Najwyższy punkt: {self.flyby_data["highest_point_time"]}, wysokość: {self.flyby_data["highest_point_altitude"]}\n' \
                       f'Jasność w najwyższym punkcie: {self.flyby_data["brightness"]}'

        logging.info(self.content)

        return self.content

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
        message.set_content(self.content)
        message.set_charset('utf-8')

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
            logging.info('Wiadomość (powiadomienie) została wysłana poprawnie.')
