from pydantic import BaseModel


class Line(BaseModel):
    id: int
    name: str
    color: str

    def update_line(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
