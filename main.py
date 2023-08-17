import sys
from typing import List
from cache import Cache
import requests as re
from requests import Response


class Scheduler:
    ENTRY_SEPERATOR: str = "BEGIN:VEVENT"
    DATA_ENCODING: str = "utf-8"


    def __init__(self) -> None:
        self.cache = Cache()
            
        self.schedules: List[str] = [
            "https://cloud.timeedit.net/liu/web/schema/ri66XXQ9678Z57Qm7X025626y6Y750322Y75Y6gQ0076927ZX4642n02X206Q08Z196772.ics",
        ]

    def _get_data_from_links(self) -> List[str]:
        return [re.get(schedule).content.decode(self.DATA_ENCODING) for schedule in self.schedules]

    def get_next_entry(self) -> str:
        """Get the next calendar entry"""
        self._get_data_from_links()


if __name__ == "__main__":
    s = Scheduler()

    s.get_next_entry()
