from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By


logging.basicConfig(level=logging.INFO)


def find_flyby(sattelite_id: str, latitude: str, longitude: str):
    """
    Scrapes flyby information from a webpage.

    Args:
        sattelite_id (str): the id of sattelite for which the flyby will be checked
        latitude (str): the latitude for which the satellite flyby will be checked
        longitude (str): the longitude for which the satellite flyby will be checked

    Returns:
        dict: flyby information
    """

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    webpage = f'https://heavens-above.com/PassSummary.aspx?satid={sattelite_id}&lat={latitude}8&lng={longitude}&loc=Unnamed&alt=0&tz=CET'
    driver.get(webpage)

    row = driver.find_element(By.CLASS_NAME, "clickableRow").text
    driver.quit()

    row = row.split(' ')
    flyby_brightness = row[2]
    flyby_start_time = row[3]
    flyby_start_altitude = row[4]
    flyby_max_time = row[6]
    flyby_max_altitude = row[7]
    flyby_end_time = row[9]
    flyby_end_altitude = row[10]

    parsed_flyby_start_time = datetime.strptime(flyby_start_time, "%H:%M:%S")
    parsed_flyby_end_time = datetime.strptime(flyby_end_time, "%H:%M:%S")
    flyby_duration = str(parsed_flyby_end_time - parsed_flyby_start_time)

    return {
        "flyby_brightness": flyby_brightness,
        "flyby_start_time": flyby_start_time,
        "flyby_start_altitude": flyby_start_altitude,
        "flyby_max_time": flyby_max_time,
        "flyby_max_altitude": flyby_max_altitude,
        "flyby_end_time": flyby_end_time,
        "flyby_end_altitude": flyby_end_altitude,
        "flyby_duration": flyby_duration
    }
