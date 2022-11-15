from pydantic import BaseModel

from .station import Station


class Line(BaseModel):
    id: int
    name: str
    color: str

    def update_line(self, name: str, color: str) -> None:
        self.name = name
        self.color = color


class LineResponse(BaseModel):
    id: int
    name: str
    color: str
    stations: list[Station]
