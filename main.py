from smtplib import SMTPAuthenticationError
import logging
from notification import Notification
from subscriber import Subscriber
from scrapper import scrap_site

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    subscribers = [
        Subscriber('Name_of_subscriber', 'email@ofsubscriber.com'),
    ]

    scrapped_data = scrap_site("Warszawa")
    if scrapped_data:
        notification = Notification(scrapped_data=scrapped_data)
        for subscriber in subscribers:
            try:
                notification.send_mail_to(subscriber)
            except SMTPAuthenticationError as e:
                logging.error(e)
