from unittest.mock import patch, MagicMock
import pytest
from notification import Notification
from scrapper import Scrapper


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    driver.find_element.return_value.text = "26 kwi -2,3 03:55:10 14° SSW 03:57:14 26° SSE 04:00:03 10° E widoczny"
    return driver


@patch('driver.Driver')
def test_find_flyby(mock_driver_class, mock_driver):
    mock_driver_instance = mock_driver
    mock_driver_class.return_value = mock_driver_instance
    scrapper = Scrapper(mock_driver_instance)
    flyby_data = scrapper.find_flyby("25544", "50.5118", "18.0665")
    assert flyby_data == {
        "brightness": "-2,3",
        "start_time": "03:55:10",
        "start_altitude": "14°",
        "highest_point_time": "03:57:14",
        "highest_point_altitude": "26°",
        "end_time": "04:00:03",
        "end_altitude": "10°",
        "duration": "0:04:53"
    }


def test_create_notification():
    flyby_data = {
        'brightness': '-2,3',
        'start_time': '03:55:10',
        'start_altitude': '14°',
        'highest_point_time': '03:57:14',
        'highest_point_altitude': '26°',
        'end_time': '04:00:03',
        'end_altitude': '10°',
        'duration': '0:04:53'
    }
    notification = Notification(flyby_data=flyby_data)
    assert notification.content == f'Początek widoczności: 03:55:10, wysokość: 14°\n' \
                                   f'Koniec widoczności: 04:00:03, wysokość: 10°\n' \
                                   f'Długość przelotu: 0:04:53\n' \
                                   f'Najwyższy punkt: 03:57:14, wysokość: 26°\n' \
                                   f'Jasność w najwyższym punkcie: -2,3'
