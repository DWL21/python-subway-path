from .line import Line

lines: dict[int, Line] = dict()
key = 1


def save_line(name: str, color: str) -> Line:
    global key
    line: Line = Line(id=key, name=name, color=color)
    key += 1
    lines[line.id] = line
    return lines[line.id]


def find_all_lines() -> list[Line]:
    return list(lines.values())


def find_line_by_id(line_id: int) -> Line | None:
    if line_id not in lines:
        raise LineNotFoundException()
    return lines[line_id]


def update_line(line_id: int, name: str, color: str) -> None:
    line: Line = find_line_by_id(line_id)
    line.update_line(name, color)


def remove_line(line_id: int) -> None:
    if line_id not in lines:
        raise LineNotFoundException()
    lines.pop(line_id)


class LineNotFoundException(Exception):
    pass
