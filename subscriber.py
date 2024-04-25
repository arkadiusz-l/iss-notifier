from dataclasses import dataclass


@dataclass
class Subscriber:
    """Represents a person who wants to receive the notifications"""

    name: str
    email: str
    object: str
    lat: str
    long: str
