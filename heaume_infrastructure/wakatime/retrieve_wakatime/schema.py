from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class Shard(BaseModel):
    duration: float
    project: str

    def add_duration(self, duration: float) -> "Shard":
        """Create a new Shard object with the add of both old and new durations.

        :param duration: The new duration.
        :type duration: float
        :return: The new Duration.
        :rtype: Duration
        """
        return Shard(duration=self.duration + duration, project=self.project)

    def to_influx_point(self, now: datetime) -> Dict[str, Any]:
        """Convert the shard to an influx point.

        :param now: The now value.
        :type now: datetime
        :return: The influx point.
        :rtype: Dict[str, Any]
        """
        return {
            "measurement": "duration",
            "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {"amount": float(self.duration)},
            "tags": {
                "provider": "wakatime",
                "unit": "second",
                "project": self.project,
                "type": "programming",
            },
            "cast": "float",
        }


class Result(BaseModel):
    data: List[Shard]

    def merged_shards(self) -> List[Shard]:
        """Merge the shards to get one duration per project name.

        :return: The list of merged shards.
        :rtype: List[Shard]
        """
        shards = {}
        for shard in self.data:
            try:
                shards[shard.project] = shards[shard.project].add_duration(shard.duration)
            except KeyError:
                shards[shard.project] = shard
        return list(shards.values())
