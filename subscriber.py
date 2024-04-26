from dataclasses import dataclass


@dataclass
class Subscriber:
    """Represents a person who wants to receive the notifications"""

    name: str
    email: str
    satellite_id: str
    latitude: str
    longitude: str
