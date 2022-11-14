from fastapi import FastAPI, Response, status, Body
from fastapi.middleware.cors import CORSMiddleware

from domain.station_dao import create, find_all, delete, StationNotFoundException
from domain.station import Station

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
    return create(name)


@app.get("/stations")
def show_all_stations() -> list[Station]:
    return find_all()


@app.delete("/stations/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(station_id: int, response: Response) -> None:
    try:
        delete(station_id)
    except StationNotFoundException:
        response.status_code = status.HTTP_404_NOT_FOUND
