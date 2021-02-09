import os

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
                "timestamp": 1609165984,
                "fields": {
                    "amount": 17
                },
                "tags": {
                    "unit": "USD",
                    "provider": "AWS",
                    "service": "Cloudformation"
                }
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
                timestamp=point["timestamp"],
                fields=point["fields"],
                tags=point["tags"],
            )
        )

    write_api.write(bucket, organization, points)

    return {"points": len(points)}


def create_point(measurement, timestamp, fields, tags):
    """Create a point for influxDB database.

    :param measurement: The name of the measurement.
    :type measurement: str
    :param timestamp: When the point happened.
    :type timestamp: str
    :param fields: The dict of fields.
    :type fields: dict
    :param tags: The dict of tags.
    :type tags: dict
    """
    point = Point(measurement).time(timestamp, WritePrecision.S)
    for k, v in fields.items():
        point = point.field(k, v)
    for k, v in tags.items():
        point = point.tag(k, v)

    return point
