import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


class Scrapper:

    @staticmethod
    def find_flyby_row(satellite_id: str, latitude: str, longitude: str) -> str:
        """
        Scrapes flyby information from a webpage.

        Args:
            satellite_id (str): the id of sattelite for which the flyby will be checked
            latitude (str): the latitude for which the satellite flyby will be checked
            longitude (str): the longitude for which the satellite flyby will be checked

        Returns:
            dict: flyby information
        """

        webpage = f"https://heavens-above.com/PassSummary.aspx?satid={satellite_id}&lat={latitude}8&lng={longitude}&loc=Unnamed&alt=0&tz=CET"
        response = requests.get(webpage)
        soup = BeautifulSoup(response.content, "html.parser")
        row = soup.find(class_="clickableRow").get_text()

        logging.debug(f"{row=}")
        return row

    @staticmethod
    def parse_flyby_row(row: str) -> dict:
        """
        Parse a row of flyby data.

        Args:
            row (str): A string containing the flyby data in a specific format

        Returns:
            dict: A dictionary containing the parsed flyby data
        """

        brightness = row[6:10]
        start_time = row[10:18]
        start_altitude = row[18:21]
        highest_point_time = row[24:32]
        highest_point_altitude = row[32:35]
        end_time = row[37:45]
        end_altitude = row[45:48]

        parsed_start_time = datetime.strptime(start_time, "%H:%M:%S")
        parsed_end_time = datetime.strptime(end_time, "%H:%M:%S")
        duration = str(parsed_end_time - parsed_start_time)

        flyby_data = {
            "brightness": brightness,
            "start_time": start_time,
            "start_altitude": start_altitude,
            "highest_point_time": highest_point_time,
            "highest_point_altitude": highest_point_altitude,
            "end_time": end_time,
            "end_altitude": end_altitude,
            "duration": duration
        }

        logging.debug(f"{flyby_data=}")
        return flyby_data
