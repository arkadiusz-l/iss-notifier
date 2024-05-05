from sqlalchemy import MetaData, Table, Column, Integer, String


def create_database(engine):
    meta = MetaData()

    subscribers = Table(
        "subscribers", meta,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("email", String),
        Column("latitude", Integer),
        Column("longitude", Integer)
    )

    satellites = Table(
        "satellites", meta,
        Column("norad_id", Integer, primary_key=True),
    )

    flybys = Table(
        "flybys", meta,
        Column("id", Integer, primary_key=True),
        Column("norad_id", Integer),
        Column("brightness", String),
        Column("start_time", String),
        Column("start_altitude", String),
        Column("highest_point_time", String),
        Column("highest_point_altitude", String),
        Column("end_time", String),
        Column("end_altitude", String),
        Column("duration", String)
    )

    subscribers_satellites = Table(
        "subscribers_satellites", meta,
        Column("id", Integer, primary_key=True),
        Column("subscriber_id", Integer),
        Column("norad_id", Integer)
    )

    subscribers_flybys = Table(
        "subscribers_flybys", meta,
        Column("id", Integer, primary_key=True),
        Column("subscriber_id", Integer),
        Column("flyby_id", Integer)
    )

    meta.create_all(engine)
    print("Database with tables has been created successfully.")

    return engine
