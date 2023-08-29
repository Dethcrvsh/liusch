import sys
from typing import List
from cache import Cache
from schedule import Schedule
from data_fetcher import DataFetcher, ScheduleData


class Scheduler:
    USE_WHITELIST: bool = True


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
        course_code: str = entry.course_codes[0]

        if self.USE_WHITELIST:
            course_code: str = self._get_whitelisted_course(entry.course_codes)

        if not course_code:
            return ""

        return f"{entry.start_date} | {entry.start_time}-{entry.end_time} | {course_code} | {entry.course_type} | {entry.locations[0]}"

    def parse_args(self, argv: List[str]) -> None:
        # Exit if there are no arguments
        if len(argv) <= 1:
            print(self.get_next_entry())
            return

        match argv[1]:
            case "--add-schedule":
                self._add_schedule(argv[2:])
            case "--add-course":
                self._add_courses(argv[2:])
            case "--remove-schedule":
                self._remove_schedule(argv[2:])
            case "--remove-course":
                self._remove_courses(argv[2:])
            case "--list-schedules":
                self._list_schedules(len(argv) > 2 and argv[2] == "links")
            case "--list-courses":
                print(self.cache.get_courses())
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

    def _add_courses(self, courses: List[str]) -> None:
        for course in courses:
            self.cache.add_course(course)

    def _remove_schedule(self, schedules: List[str]) -> None:
        for schedule in schedules:
            name: str = schedule

            self.cache.remove_schedule(name)

    def _remove_courses(self, courses: List[str]) -> None:
        for course in courses:
            self.cache.remove_course(course)

    def _list_schedules(self, show_links: bool) -> None:
        for schedule in self.cache.get_schedules():
            if show_links:
                print("{:<24} {}".format(schedule.name, schedule.link))
            else:
                print(schedule.name)

    def _get_whitelisted_course(self, courses: List[str]) -> str:
        """Get the course that's in the whitelist from a list of courses"""
        whitelist: List[str] = self.cache.get_courses()

        for course in courses:
            print(f"{course} in {whitelist}")
            if course in whitelist:
                return course

        return ""


if __name__ == "__main__":
    scheduler: Scheduler = Scheduler()
    scheduler.parse_args(sys.argv)

