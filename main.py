from smtplib import SMTPAuthenticationError
import logging
from notification import Notification
from subscriber import Subscriber
from scrapper import find_flyby

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    subscribers = [
        Subscriber('Name_of_subscriber', 'email@ofsubscriber.com'),
    ]

    flyby_data = find_flyby(satellite_id="25544", latitude="52.2320", longitude="21.0067")
    if flyby_data:
        notification = Notification(flyby_data=flyby_data)
        for subscriber in subscribers:
            try:
                notification.send_mail_to(subscriber)
            except SMTPAuthenticationError as e:
                logging.error(e)
