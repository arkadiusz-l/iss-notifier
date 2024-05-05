from sqlalchemy import create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine("sqlite:///database.db", echo=False, future=True)
Base = declarative_base()


class SubscriberModel(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    email = Column(String(50))
    latitude = Column(String(7))
    longitude = Column(String(7))
    subscriber_satellite = relationship("SubscribersSatellitesModel", back_populates="subscriber")


class SatelliteModel(Base):
    __tablename__ = "satellites"
    norad_id = Column(Integer, primary_key=True, autoincrement=False)
    subscriber_satellite = relationship("SubscribersSatellitesModel", back_populates="satellite")


class FlybyModel(Base):
    __tablename__ = "flybys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    norad_id = Column(Integer, ForeignKey("satellites.norad_id"))
    brightness = Column(String(4))
    start_time = Column(String(8))
    start_altitude = Column(String(3))
    highest_point_time = Column(String(8))
    highest_point_altitude = Column(String(3))
    end_time = Column(String(8))
    end_altitude = Column(String(3))
    duration = Column(String(7))


class SubscribersSatellitesModel(Base):
    __tablename__ = "subscribers_satellites"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))
    norad_id = Column(Integer, ForeignKey("satellites.norad_id"))
    subscriber = relationship("SubscriberModel", back_populates="subscriber_satellite")
    satellite = relationship("SatelliteModel", back_populates="subscriber_satellite")


class SubscribersFlybysModel(Base):
    __tablename__ = "subscribers_flybys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))
    flyby_id = Column(Integer, ForeignKey("flybys.id"))
