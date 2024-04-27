import json
import logging
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused
from notification import Notification
from scrapper import Scrapper
from subscriber import Subscriber

logging.basicConfig(level=logging.INFO)


def load_subscribers(file: str) -> list:
    try:
        with open(file, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error("File not found!")

    return data["subscribers"]


if __name__ == "__main__":
    subscribers = load_subscribers("subscribers.json")
    scrapper = Scrapper()
    notification = None

    for subscriber in subscribers:
        subscriber = Subscriber(
            name=subscriber["name"],
            email=subscriber["email"],
            satellite_id=subscriber["satellite_id"],
            latitude=subscriber["localization"]["latitude"],
            longitude=subscriber["localization"]["longitude"]
        )

        flyby_row = scrapper.find_flyby_row(
            satellite_id=subscriber.satellite_id,
            latitude=subscriber.latitude,
            longitude=subscriber.longitude
        )

        flyby_row = scrapper.parse_flyby_row(flyby_row)

        if flyby_row:
            notification = Notification(flyby_data=flyby_row)
        try:
            notification.send_mail_to(subscriber)
        except SMTPAuthenticationError as error:
            logging.error(error)
        except SMTPRecipientsRefused as error:
            logging.error(error)
