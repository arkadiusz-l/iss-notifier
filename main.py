import json
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused
import logging
from notification import Notification
from subscriber import Subscriber
from scrapper import find_flyby

logging.basicConfig(level=logging.INFO)


def load_subscribers(file: str) -> list:
    try:
        with open(file, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error("File not found!")

    return data["subscribers"]


if __name__ == '__main__':
    subscribers = load_subscribers("subscribers.json")
    notification = None

    for subscriber in subscribers:
        subscriber = Subscriber(
            name=subscriber["name"],
            email=subscriber["email"],
            satellite_id=subscriber["satellite_id"],
            latitude=subscriber["localization"]["latitude"],
            longitude=subscriber["localization"]["longitude"]
        )

        flyby_data = find_flyby(
            satellite_id=subscriber.satellite_id,
            latitude=subscriber.latitude,
            longitude=subscriber.longitude
        )

        if flyby_data:
            notification = Notification(flyby_data=flyby_data)
        try:
            notification.send_mail_to(subscriber)
        except SMTPAuthenticationError as error:
            logging.error(error)
        except SMTPRecipientsRefused as error:
            logging.error(error)
