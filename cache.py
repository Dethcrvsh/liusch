import os
import json
from typing import List
from dataclasses import dataclass


@dataclass
class Schedule:
    name: str = ""
    link: str = ""

    def to_json(self) -> str:
        return f"({self.name},{self.link})"

    def from_json(self, data: str):
        self.name: str = data[1:data.find(",")]
        self.link: str = data[data.find(",") + 1:-1]
        
        return self


class Cache:
    DIR_NAME: str = "python-liu-schedule"
    FILE_NAME: str = "schedules.json"


    def __init__(self) -> None:
        self.dir: str = self._init_cache_dir()
        self.file: str = os.path.join(self.dir, self.FILE_NAME)


    def add_schedule(self, name: str, link: str) -> None:
        data: List[Schedule] = self._read()
        data.append(Schedule(name, link))
        self._write(data)


    def _read(self) -> List[Schedule]:
        data: List[str] = []

        try:
            with open(self.file, "r") as file:
                data: List[str] = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data: List[str] = []

        return [Schedule().from_json(schedule) for schedule in data]

    
    def _write(self, schedule_links: List[Schedule]) -> None:
        with open(self.file, "w") as file:
            json.dump(schedule_links, file, default=lambda o: o.to_json())


    def _init_cache_dir(self) -> str:
        # Get the home catalogue path
        home: str | None = os.getenv("HOME", os.getenv("USERPROFILE"))

        if home is None:
            raise FileNotFoundError("Home catalogue could not be found.")

        # Get the cache directory path
        cache_dir: str = os.getenv("XDG_CACHE_HOME", os.path.join(home, ".cache"))

        if cache_dir is None:
            raise FileNotFoundError("Cache directory could not be found.")

        cache_dir: str = os.path.join(cache_dir, self.DIR_NAME)
        
        # Create the directory if it does not exist
        os.makedirs(cache_dir, exist_ok=True)

        return cache_dir
