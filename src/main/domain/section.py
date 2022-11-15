from pydantic import BaseModel


class Section(BaseModel):
    id: int
    upStationId: int
    downStationId: int
    distance: int
    line_id: int

    def equals_line_id(self, line_id: int) -> bool:
        return self.line_id == line_id

    def slice_right(self, section) -> None:
        self.upStationId = section.downStationId
        self.distance -= section.distance

    def slice_left(self, section) -> None:
        self.downStationId = section.upStationId
        self.distance -= section.distance
