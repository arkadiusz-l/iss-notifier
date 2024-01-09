from datetime import datetime
from time import sleep
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions

logging.basicConfig(level=logging.INFO)


def scrap_site(localization: str):
    """
    Scrapes flyby information from a website, for given localization.

    Args:
        localization (str): the location for which the flyby will be checked

    Returns:
        dict: flyby information
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    webpage = 'https://isstracker.pl/iss/godziny-przelotow/polska'
    driver.get(webpage)

    try:
        driver.find_element(By.CLASS_NAME, value="fc-button-label").click()
    except selenium.common.exceptions.NoSuchElementException:
        pass

    search_input = driver.find_element(By.XPATH, "//input[@id='autocomplete']")
    search_input.send_keys(localization)
    sleep(2)
    search_input.send_keys(Keys.ENTER)
    sleep(2)

    alert = driver.find_element(By.XPATH, "//div[@class='mt-3 alert alert-info']").text
    if alert.startswith("Niestety brak przelotów"):
        return

    city = driver.find_element(By.XPATH, "//div[@class='alert alert-success']").text
    flight = driver.find_element(By.XPATH, "//div[@class='col-md-8 col-sm-12']").text
    brightness = driver.find_element(By.XPATH, "//div[@class='col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12']//li[3]").text
    max_altitude = driver.find_element(By.XPATH, "//div[@class='col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12']//li[4]").text
    driver.quit()

    city = city.split(' ')
    city = city[6:-5]
    city = ' '.join(city)

    flight = flight.split('\n')
    flight = flight[0:-1]

    flight_date_time, flight_duration, flight_period = flight
    flight_period = flight_period.split(' K')
    flight_start, flight_end = flight_period
    flight_end = 'K' + flight_end

    name_start, date_time_start = flight_start.split(': ')
    name_end, date_time_end = flight_end.split(': ')

    date_start, time_start = date_time_start.split(' ')
    date_end, time_end = date_time_end.split(' ')

    date_time_start = datetime.strptime(date_time_start, '%Y-%m-%d %H:%M:%S')

    flight_date_time = flight_date_time.split(' ')
    flight_date, flight_time = flight_date_time
    year, month, day = flight_date.split('-')
    flight_date_pl = f'{day}.{month}.{year}'

    time_to_flight = str(date_time_start - datetime.now())
    time_to_flight = time_to_flight.split(':')

    max_altitude = max_altitude.split(":")[1]

    logging.info(f"Poproszono o '{localization}', otrzymano '{city}'.")

    return {
        "flight_date_pl": flight_date_pl,
        "city": city,
        "name_start": name_start,
        "time_start": time_start,
        "name_end": name_end,
        "time_end": time_end,
        "flight_duration": flight_duration,
        "time_to_flight": time_to_flight,
        "brightness": brightness,
        "max_altitude": max_altitude,
    }
