from fastapi import FastAPI, status, Body
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from domain.station import Station
from domain.station_dao import save_station, find_station_by_id, find_all_stations, remove_station, \
    StationNotFoundException
from domain.line import Line, LineResponse
from domain.line_dao import save_line, find_all_lines, find_line_by_id, update_line, remove_line, LineNotFoundException
from domain.section import Section
from domain.sections import Sections
from domain.section_dao import save_section, find_sections_by_line_id, remove_section, remove_sections

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/stations", status_code=status.HTTP_201_CREATED)
def create_station(name: str = Body(embed=True)) -> Station:
    return save_station(name)


@app.get("/stations")
def show_all_stations() -> list[Station]:
    return find_all_stations()


@app.delete("/stations/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(station_id: int, response: Response) -> None:
    try:
        remove_station(station_id)
    except StationNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.post("/lines", status_code=status.HTTP_201_CREATED)
def create_line(name: str = Body(embed=True), color: str = Body(embed=True), upStationId: int = Body(embed=True),
                downStationId: int = Body(embed=True), distance: int = Body(embed=True)) -> Line:
    line: Line = save_line(name, color)
    save_section(line.id, upStationId, downStationId, distance)
    return line


@app.get("/lines")
def show_all_lines() -> list[LineResponse]:
    responses: list[LineResponse] = list()
    for line in find_all_lines():
        responses.append(
            LineResponse(id=line.id, name=line.name, color=line.color, stations=find_all_stations_in_line(line.id)))
    return responses


@app.get("/lines/{line_id}")
def show_line(line_id: int, response: Response) -> LineResponse | None:
    try:
        line: Line = find_line_by_id(line_id)
        return LineResponse(id=line.id, name=line.name, color=line.color, stations=find_all_stations_in_line(line_id))
    except LineNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND


def find_all_stations_in_line(line_id: int):
    sections: Sections = find_sections_by_line_id(line_id)
    stations: list[Station] = list()
    for station_id in set(sections.get_all_stations()):
        stations.append(find_station_by_id(station_id))
    return stations


@app.put("/lines/{line_id}")
def put_line(line_id: int, response: Response, name: str = Body(embed=True), color: str = Body(embed=True)) -> None:
    try:
        update_line(line_id, name, color)
    except LineNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.delete("/lines/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_line(line_id: int, response: Response) -> None:
    try:
        remove_line(line_id)
        remove_sections(line_id)
    except LineNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.post("/lines/{line_id}/sections")
def register(line_id: int, upStationId: int = Body(embed=True),
             downStationId: int = Body(embed=True), distance: int = Body(embed=True)) -> None:
    section: Section = save_section(line_id, upStationId, downStationId, distance)
    sections: Sections = find_sections_by_line_id(line_id)
    sections.register_section(section)


@app.delete("/lines/{line_id}/sections")
def delete(line_id: int, stationId: int) -> None:
    remove_section(line_id, stationId)
