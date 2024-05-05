import json
import logging
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused
from sys import argv
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from install import create_database
from models import FlybyModel, SubscriberModel, SatelliteModel, SubscribersSatellitesModel
from notification import Notification
from scrapper import Scrapper

logging.basicConfig(level=logging.INFO)


def load_subscribers(file: str) -> list:
    try:
        with open(file, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error("File not found!")

    return data["subscribers"]


def load_models_to_database(db):
    for subscriber in subscribers:
        subscriber_model = SubscriberModel(
            name=subscriber["name"],
            email=subscriber["email"],
            latitude=subscriber["location"]["latitude"],
            longitude=subscriber["location"]["longitude"]
        )

        with Session(db) as session:
            session.commit()
            session.add(subscriber_model)

            for satellite in subscriber["satellites"]:
                existing_satellite = session.query(SatelliteModel).filter_by(norad_id=satellite["norad_id"]).first()
                if not existing_satellite:
                    satellite_model = SatelliteModel(
                        norad_id=satellite["norad_id"],
                    )
                    session.add(satellite_model)

                subscribers_satellites = SubscribersSatellitesModel(
                    subscriber_id=subscriber_model.id,
                    norad_id=satellite["norad_id"]
                )
                session.add(subscribers_satellites)
                session.commit()
    logging.info("Models have been loaded successfully.")


if __name__ == "__main__":
    db_engine = create_engine("sqlite:///database.db", echo=False, future=True)
    if len(argv) > 1 and argv[1] == "install":
        create_database(db_engine)

    subscribers = load_subscribers("subscribers.json")
    scrapper = Scrapper()
    notification = None

    load_models_to_database(db_engine)

    with Session(db_engine) as session:
        all_subscribers_satellites = session.query(SubscribersSatellitesModel).all()

        for item in all_subscribers_satellites:
            item_latitude, item_longitude = session.query(
                SubscriberModel.latitude, SubscriberModel.longitude
            ).filter(
                SubscriberModel.id == session.query(
                    SubscribersSatellitesModel.subscriber_id
                ).filter(
                    SubscribersSatellitesModel.id == 1
                ).scalar_subquery()
            ).first()
            logging.debug(f"{item_latitude=}")
            logging.debug(f"{item_latitude=}")

            flyby_row = scrapper.find_flyby_row(
                satellite_id=item.norad_id,
                latitude=item_latitude,
                longitude=item_longitude
            )
            logging.debug(f"{flyby_row=}")

            flyby_data = scrapper.parse_flyby_row(flyby_row)

            flyby_model = FlybyModel(
                norad_id=item.norad_id,
                brightness=flyby_data["brightness"],
                start_time=flyby_data["start_time"],
                start_altitude=flyby_data["start_altitude"],
                highest_point_time=flyby_data["highest_point_time"],
                highest_point_altitude=flyby_data["highest_point_altitude"],
                end_time=flyby_data["end_time"],
                end_altitude=flyby_data["end_altitude"],
                duration=flyby_data["duration"]
            )
            session.add(flyby_model)
            session.commit()
            sleep(1)

    if flyby_data:
        notification = Notification(flyby_data=flyby_data)
    try:
        notification.send_mail_to(SubscriberModel.email)
    except SMTPAuthenticationError as error:
        logging.error(error)
    except SMTPRecipientsRefused as error:
        logging.error(error)
