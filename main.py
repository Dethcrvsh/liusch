import sys
from typing import List
from cache import Cache
from schedule import Schedule
from data_fetcher import DataFetcher, ScheduleData


class Scheduler:
    def __init__(self) -> None:
        self.cache: Cache = Cache()
        self.data_fetcher: DataFetcher = DataFetcher()
            
    def get_next_entry(self) -> str:
        """Get the next calendar entry"""
        data: List[ScheduleData] = self.data_fetcher.get_data(self.cache.get_schedules())

        if not data:
            return ""

        entry: ScheduleData = data[0]

        # TODO: Handle several course codes and locations
        return f"{entry.start_date} | {entry.start_time}-{entry.end_time} | {entry.course_codes[0]} | {entry.course_type} | {entry.locations[0]}"

    def parse_args(self, argv: List[str]) -> None:
        # Exit if there are no arguments
        if len(argv) <= 1:
            print(self.get_next_entry())
            return

        match argv[1]:
            case "--add-schedule":
                self._add_schedule(argv[2:])
            case "--remove-schedule":
                self._remove_schedule(argv[2:])
            case "--list-schedules":
                self._list_schedules()
            case _:
                print(f"{argv[1]} is not a valid argument.")

    def _add_schedule(self, schedules: List[str]) -> None:
        if not len(schedules) % 2 == 0:
            print("Names and links do not match.")
            return

        for i in range(0, len(schedules), 2):
            name: str = schedules[i]
            link: str = schedules[i + 1]

            self.cache.add_schedule(name, link)

    def _remove_schedule(self, schedules: List[str]) -> None:
        for schedule in schedules:
            name: str = schedule

            self.cache.remove_schedule(name)

    def _list_schedules(self) -> None:
        for schedule in self.cache.get_schedules():
            print(schedule.name)


if __name__ == "__main__":
    scheduler: Scheduler = Scheduler()
    scheduler.parse_args(sys.argv)

