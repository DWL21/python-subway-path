from fastapi import FastAPI, Response, status, Body
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from domain.station import Station
from domain.station_dao import save_station, find_all_stations, remove_station, StationNotFoundException
from domain.line import Line
from domain.line_dao import save_line, find_all_lines, find_line_by_id, update_line, remove_line, LineNotFoundException

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
def create_line(name: str = Body(embed=True), color: str = Body(embed=True)) -> Line:
    return save_line(name, color)


@app.get("/lines")
def show_all_lines() -> list[Line]:
    return find_all_lines()


@app.get("/lines/{line_id}")
def show_line(line_id: int, response: Response) -> Line | None:
    try:
        return find_line_by_id(line_id)
    except LineNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND


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
    except LineNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND
