from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


logging.basicConfig(level=logging.INFO)


def find_flyby(satellite_id: str, latitude: str, longitude: str) -> dict:
    """
    Scrapes flyby information from a webpage.

    Args:
        satellite_id (str): the id of sattelite for which the flyby will be checked
        latitude (str): the latitude for which the satellite flyby will be checked
        longitude (str): the longitude for which the satellite flyby will be checked

    Returns:
        dict: flyby information
    """

    try:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

        webpage = f'https://heavens-above.com/PassSummary.aspx?satid={satellite_id}&lat={latitude}8&lng={longitude}&loc=Unnamed&alt=0&tz=CET'
        driver.get(webpage)

        row = driver.find_element(By.CLASS_NAME, "clickableRow").text
        driver.quit()

        row = row.split(' ')
        brightness = row[2]
        start_time = row[3]
        start_altitude = row[4]
        highest_point_time = row[6]
        highest_point_altitude = row[7]
        end_time = row[9]
        end_altitude = row[10]

        parsed_start_time = datetime.strptime(start_time, "%H:%M:%S")
        parsed_end_time = datetime.strptime(end_time, "%H:%M:%S")
        duration = str(parsed_end_time - parsed_start_time)

        return {
            "brightness": brightness,
            "start_time": start_time,
            "start_altitude": start_altitude,
            "highest_point_time": highest_point_time,
            "highest_point_altitude": highest_point_altitude,
            "end_time": end_time,
            "end_altitude": end_altitude,
            "duration": duration
        }

    except WebDriverException:
        logging.error("Webpage not reached!")
