import json
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused
import logging
from notification import Notification
from subscriber import Subscriber
from scrapper import find_flyby

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        with open("subscribers.json", encoding="utf-8") as file:
            data = json.load(file)

        subscribers = data["subscribers"]

        for subscriber in subscribers:
            subscriber = Subscriber(
                name=subscriber["name"],
                email=subscriber["email"],
                object=subscriber["object"],
                lat=subscriber["loc"]["lat"],
                long=subscriber["loc"]["long"]
            )

            flyby_data = find_flyby(
                satellite_id=subscriber.object,
                latitude=subscriber.lat,
                longitude=subscriber.long
            )

            if flyby_data:
                notification = Notification(flyby_data=flyby_data)
                notification.send_mail_to(subscriber)
    except FileNotFoundError:
        logging.error("File not found!")
    except SMTPAuthenticationError as error:
        logging.error(error)
    except SMTPRecipientsRefused as error:
        logging.error(error)
