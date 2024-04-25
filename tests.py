from unittest.mock import patch, MagicMock
import pytest
from notification import Notification
from scrapper import find_flyby


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    driver.find_element.return_value.text = "26 kwi -2,3 03:55:10 14° SSW 03:57:14 26° SSE 04:00:03 10° E widoczny"
    return driver


@patch('scrapper.webdriver')
def test_find_flyby(mock_webdriver, mock_driver):
    mock_webdriver.Firefox.return_value = mock_driver
    flyby_data = find_flyby("25544", "50.5118", "18.0665")
    assert flyby_data == {
        "flyby_brightness": "-2,3",
        "flyby_start_time": "03:55:10",
        "flyby_start_altitude": "14°",
        "flyby_max_time": "03:57:14",
        "flyby_max_altitude": "26°",
        "flyby_end_time": "04:00:03",
        "flyby_end_altitude": "10°",
        "flyby_duration": "0:04:53"
    }


def test_create_notification():
    flyby_data = {
        'flyby_brightness': '-2,3',
        'flyby_start_time': '03:55:10',
        'flyby_start_altitude': '14°',
        'flyby_max_time': '03:57:14',
        'flyby_max_altitude': '26°',
        'flyby_end_time': '04:00:03',
        'flyby_end_altitude': '10°',
        'flyby_duration': '0:04:53'
    }

    notification = Notification(flyby_data=flyby_data)
    notification = notification.create()

    assert notification == f'Początek przelotu: 03:55:10\n' \
                           f'Koniec przelotu: 04:00:03\n' \
                           f'Długość przelotu: 0:04:53\n' \
                           f'Jasność w najwyższym punkcie: -2,3\n' \
                           f'Max wysokość nad horyzontem: 26°'
