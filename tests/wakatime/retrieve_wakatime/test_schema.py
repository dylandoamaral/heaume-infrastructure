from heaume_infrastructure.wakatime.retrieve_wakatime.schema import Result, Shard
from pytest import fixture
from datetime import datetime


def describe_schemas():
    @fixture
    def result():
        return Result(
            data=[
                Shard(project="project1", duration=100),
                Shard(project="project2", duration=140),
                Shard(project="project3", duration=110),
                Shard(project="project2", duration=140),
                Shard(project="project1", duration=210),
            ]
        )

    def describe_result():
        def merged_shards(result):
            shards = sorted(result.merged_shards(), key=lambda shard: shard.project)
            assert shards == [
                Shard(project="project1", duration=310),
                Shard(project="project2", duration=280),
                Shard(project="project3", duration=110),
            ]

    def describe_shards():
        def add_duration(result):
            shard = result.data[0]
            new_shard = shard.add_duration(200)
            assert new_shard.duration == 300

        def to_influx_point(result):
            shard = result.data[0]
            now = datetime(2021, 1, 1)
            point = shard.to_influx_point(now)
            print(point)
            assert point == {
                "cast": "float",
                "time": "2021-01-01T00:00:00Z",
                "fields": {"amount": 100.0},
                "measurement": "duration",
                "tags": {
                    "project": "project1",
                    "provider": "wakatime",
                    "type": "programming",
                    "unit": "second",
                },
                "cast": "float",
            }
