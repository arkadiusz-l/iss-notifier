import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)


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

        Note:
            The removal of all letters from index 6 to the end is necessary because directions sometimes have
            single-letter designations (e.g. E) and sometimes three-letter designations (e.g. ESE),
            which changes the length of string and causes issues with slicing.
            These letters are currently unnecessary.
        """

        row = row[:6] + "".join([char for char in row[6:] if not char.isalpha()])
        row = row.split("°")

        logging.debug(f"{row=}")

        brightness_first_sign = row[0][6]
        if brightness_first_sign == "?":
            brightness = "nieznana"
        elif brightness_first_sign.isnumeric():
            brightness = "+" + row[0][6:9]
        else:
            brightness = row[0][6:10]
        start_time = row[0][-10:-2]
        start_altitude = row[0][-2:]
        highest_point_time = row[1][:-2]
        highest_point_altitude = row[1][-2:]
        end_time = row[2][:-2]
        end_altitude = row[2][-2:]

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
