from .station import Station

stations: dict[int, Station] = dict()
key = 1


def save_station(name: str) -> Station:
    global key
    station: Station = Station(id=key, name=name)
    key += 1
    stations[station.id] = station
    return stations[station.id]


def find_all_stations() -> list[Station]:
    return list(stations.values())


def find_station_by_id(station_id: int) -> Station | None:
    if station_id not in stations:
        raise StationNotFoundException()
    return stations[station_id]


def remove_station(station_id: int) -> None:
    if station_id not in stations:
        raise StationNotFoundException()
    stations.pop(station_id)


class StationNotFoundException(Exception):
    pass
