from .section import Section


class Sections:
    def __init__(self, sections: list[Section]) -> None:
        self.up_sections: dict[int, Section] = dict()
        self.down_sections: dict[int, Section] = dict()
        for section in sections:
            self.up_sections[section.upStationId] = section
            self.down_sections[section.downStationId] = section

    def get_all_stations(self) -> list[int]:
        return list(self.up_sections.keys()) + list(self.down_sections.keys())

    def find_sections_by_station_id(self, station_id: int) -> list[Section]:
        found_section = list()
        for i in [self.up_sections, self.down_sections]:
            if station_id in i:
                found_section.append(i[station_id])
        return found_section

    def register_section(self, section: Section):
        if section.upStationId in self.up_sections:
            saved_section: Section = self.up_sections[section.upStationId]
            saved_section.slice_right(section)
        elif section.downStationId in self.down_sections:
            saved_section: Section = self.down_sections[section.downStationId]
            saved_section.slice_left(section)
