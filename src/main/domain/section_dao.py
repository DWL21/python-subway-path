from .section import Section
from .sections import Sections

sections: dict[int, Section] = dict()
key = 1


def save_section(line_id: int, upStationId: int, downStationId: int, distance: int) -> Section:
    global key
    section: Section = Section(
        id=key,
        upStationId=upStationId,
        downStationId=downStationId,
        distance=distance,
        line_id=line_id)
    sections[section.id] = section
    return sections[section.id]


def find_sections_by_line_id(line_id: int) -> Sections:
    line_sections = list(filter(lambda x: x.id == line_id, sections.values()))
    return Sections(line_sections)


def remove_section(line_id: int, station_id: int) -> None:
    found_sections: Sections = find_sections_by_line_id(line_id)
    for section in found_sections.find_sections_by_station_id(station_id):
        sections.pop(section.id)


def remove_sections(line_id: int) -> None:
    for section in find_sections_by_line_id(line_id).up_sections.values():
        sections.pop(section.id)
