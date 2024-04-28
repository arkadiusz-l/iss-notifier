from notification import Notification
from scrapper import Scrapper


def test_parse_flyby_row():
    row = "27 Apr-1.903:07:5917°SSE03:08:3318°SE03:10:5310°Evisible"
    result = Scrapper.parse_flyby_row(row)

    assert result == {
        "brightness": "-1.9",
        "start_time": "03:07:59",
        "start_altitude": "17°",
        "highest_point_time": "03:08:33",
        "highest_point_altitude": "18°",
        "end_time": "03:10:53",
        "end_altitude": "10°",
        "duration": "0:02:54"
    }


def test_create_notification():
    flyby_data = {
        "brightness": "-2,3",
        "start_time": "03:55:10",
        "start_altitude": "14°",
        "highest_point_time": "03:57:14",
        "highest_point_altitude": "26°",
        "end_time": "04:00:03",
        "end_altitude": "10°",
        "duration": "0:04:53"
    }
    notification = Notification(flyby_data=flyby_data)
    assert notification.content == f"Początek widoczności: 03:55:10, wysokość: 14°\n" \
                                   f"Koniec widoczności: 04:00:03, wysokość: 10°\n" \
                                   f"Długość przelotu: 0:04:53\n" \
                                   f"Najwyższy punkt: 03:57:14, wysokość: 26°\n" \
                                   f"Jasność w najwyższym punkcie: -2,3"
