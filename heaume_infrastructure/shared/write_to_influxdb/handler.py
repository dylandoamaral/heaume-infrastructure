import os

from cast import NoCast, cast_mapping
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def handler(event, context):
    """Write points to influxDB based on the event information.

    :Example:
    event = {
        "organization": "Heaume",
        "bucket": "DailyCost",
        "points": [
            {
                "measurement": "price",
                "time": '2021-02-09T23:59:59Z',
                "fields": {
                    "amount": 17
                },
                "tags": {
                    "unit": "USD",
                    "provider": "AWS",
                    "service": "Cloudformation"
                },
                "cast": "float"
            }
        ]
    }


    """
    organization = event["organization"]
    bucket = event["bucket"]

    client = InfluxDBClient(url=os.environ["url"], token=os.environ["token"])
    write_api = client.write_api(write_options=SYNCHRONOUS)

    points = []
    for point in event["points"]:
        points.append(
            create_point(
                measurement=point["measurement"],
                time=point["time"],
                fields=point["fields"],
                tags=point["tags"],
                cast=point.get("cast"),
            )
        )

    write_api.write(bucket, organization, points)

    return {"points": len(points)}


def create_point(measurement, time, fields, tags, cast):
    """Create a point for influxDB database.

    :param measurement: The name of the measurement.
    :type measurement: str
    :param time: When the point happened in %Y-%m-%dT%H:%M:%SZ.
    :type time: str
    :param fields: The dict of fields.
    :type fields: dict
    :param tags: The dict of tags.
    :type tags: dict
    :param cast: The potential casting requirement.
    :type cast: Optional[CastType]
    """
    point = Point(measurement).time(time, WritePrecision.S)
    cast = cast_mapping[cast] if cast else NoCast()
    for k, v in fields.items():
        point = point.field(k, cast.cast(v))
    for k, v in tags.items():
        point = point.tag(k, v)

    return point
